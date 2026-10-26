#!/usr/bin/env python3
"""Check declared development capabilities and effective image references.

Read-only source preflight. Never installs tools or certifies a Codespace.
"""
import argparse
import json
from pathlib import Path
import re
import sys
import yaml


def require(ok, why):
    if not ok:
        raise ValueError(why)


def unique(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON field')
        result[key] = value
    return result


def jsonc(raw):
    # Preserve quoted URLs and comment-like strings. Strip comments and
    # trailing commas only outside JSON strings; never execute JSON5 code.
    out=[]; i=0; quoted=False
    while i<len(raw):
        c=raw[i]
        if quoted:
            out.append(c)
            if c=='\\' and i+1<len(raw):
                i+=1;out.append(raw[i])
            elif c=='"': quoted=False
        elif c=='"': quoted=True;out.append(c)
        elif raw[i:i+2]=='//':
            end=raw.find('\n',i+2);i=len(raw) if end<0 else end;out.append('\n');continue
        elif raw[i:i+2]=='/*':
            end=raw.find('*/',i+2);require(end>=0,'unterminated JSON comment');i=end+2;out.append(' ');continue
        else: out.append(c)
        i+=1
    stripped=''.join(out);out=[];i=0;quoted=False
    while i<len(stripped):
        c=stripped[i]
        if quoted:
            out.append(c)
            if c=='\\' and i+1<len(stripped):
                i+=1;out.append(stripped[i])
            elif c=='"':quoted=False
        elif c=='"':quoted=True;out.append(c)
        elif c==',' and stripped[i+1:].lstrip().startswith(('}',']')):pass
        else:out.append(c)
        i+=1
    return json.loads(''.join(out),object_pairs_hook=unique)


def inside(root, path):
    resolved=path.resolve()
    require(resolved.is_relative_to(root.resolve()) and resolved.is_file(), 'configuration outside repository or missing')
    require(resolved.stat().st_size<=262144,'configuration too large')
    return resolved


def yaml_file(path):
    class ClosedLoader(yaml.SafeLoader):
        pass
    def mapping(loader,node,deep=False):
        pairs=[]
        for key,value in node.value:
            pairs.append((loader.construct_object(key,deep=deep),loader.construct_object(value,deep=deep)))
        return unique(pairs)
    ClosedLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,mapping)
    return yaml.load(path.read_text(),Loader=ClosedLoader)


def version(value):
    require(isinstance(value,str) and re.fullmatch(r'\d+\.\d+\.\d+',value),'exact environment version required')
    return tuple(map(int,value.split('.')))


def docker_base(root, folder, build, expected, *, relative_to_config=False):
    if isinstance(build,str): build={'context':build}
    require(isinstance(build,dict),'invalid build configuration')
    context=(folder/build.get('context','.')).resolve()
    require(context.is_relative_to(root.resolve()) and context.is_dir(),'build context outside repository or missing')
    path=inside(root,(folder if relative_to_config else context)/build.get('dockerfile','Dockerfile'))
    overrides=build.get('args',{});require(isinstance(overrides,dict),'build args mapping required')
    args={}; stages={}; final=False; started=False
    for line in path.read_text().splitlines():
        line=line.strip()
        require('<<' not in line,'Dockerfile heredoc analysis unsupported')
        if line.startswith('ARG ') and not started:
            key,sep,value=line[4:].partition('=')
            args[key]=overrides.get(key,value if sep else '')
        if not re.match(r'FROM\s',line,re.I): continue
        started=True
        fields=line.split()[1:]
        fields=[field for field in fields if not field.startswith('--platform=')]
        require(fields,'missing FROM image')
        image=re.sub(r'\$\{(\w+)\}|\$(\w+)',lambda m:str(args.get(m[1] or m[2],'')),fields[0])
        final=stages.get(image, bool(re.fullmatch(re.escape(expected)+r'(?:@sha256:[a-f0-9]{64})?',image)))
        if len(fields)==3 and fields[1].upper()=='AS': stages[fields[2]]=final
    if build.get('target') is not None: final=stages.get(build['target'],False)
    require(final,'effective Dockerfile stage does not inherit declared image')
    return expected


def effective_image(root, config, expected):
    require(isinstance(config,dict),'Dev Container must be an object')
    require(sum(k in config for k in ('image','build','dockerComposeFile'))==1,'ambiguous Dev Container source')
    if 'build' in config:
        return docker_base(root,root/'.devcontainer',config['build'],expected,relative_to_config=True)
    if 'image' in config:
        image=config['image']
        require(isinstance(image,str),'image must be text')
        return image
    files=config.get('dockerComposeFile')
    require(isinstance(files,(list,str)) and files,'image or Compose reference required')
    if isinstance(files,str): files=[files]
    service=config.get('service');require(isinstance(service,str) and service,'Compose workspace service required')
    selected={};folder=None;found=False
    for filename in files:
        require(isinstance(filename,str),'Compose file must be local text')
        path=inside(root,root/'.devcontainer'/filename)
        data=yaml_file(path)
        require(isinstance(data,dict) and 'include' not in data,'unsupported Compose include')
        if folder is None: folder=path.parent
        row=data.get('services',{}).get(service,{})
        require(isinstance(row,dict),'invalid Compose workspace')
        require('extends' not in row,'unsupported Compose service extends')
        row=dict(row)
        if isinstance(row.get('build'),str):row['build']={'context':row['build']}
        def merge(base,extra):
            result=dict(base)
            for key,value in extra.items():
                result[key]=merge(result[key],value) if isinstance(result.get(key),dict) and isinstance(value,dict) else value
            return result
        selected=merge(selected,row)
        found=found or bool(row)
    require(found,'Compose workspace service missing')
    if 'build' in selected:
        return docker_base(root,folder,selected['build'],expected)
    return selected.get('image')


def check(root, catalogue):
    root=Path(root)
    declaration=yaml_file(inside(root,root/'.baobab/environment.yaml'))
    require(isinstance(declaration,dict),'declaration must be an object')
    require(all(isinstance(declaration.get(k),dict) for k in ('schema','environment','validation')),'declaration objects required')
    require(declaration.get('schema',{}).get('name') in {
        'baobab-development-environment-contract','baobab-platform-development-environment-contract'},'invalid environment contract name')
    require(str(declaration['schema'].get('version'))=='1.0','unsupported declaration version')
    require(isinstance(declaration,dict),'declaration must be an object')
    env=declaration.get('environment',{})
    require(env.get('provider')=='baobab-dev','unsupported environment provider')
    require(catalogue.get('schema_version')==1 and catalogue.get('provider')=='baobab-dev','unsupported catalogue')
    profile=env.get('profile');require(profile in catalogue['profiles'],'unknown profile')
    policy=catalogue['profiles'][profile];suffix=policy['tag_suffix']
    declared=env.get('minimum_version','')
    require(isinstance(declared,str),'version must be text')
    bare=declared.removesuffix(suffix) if suffix else declared
    require(version(bare)>=version(policy['minimum_version']),'image below supported floor')
    required=declaration.get('validation',{}).get('required_capabilities')
    require(isinstance(required,list) and len(required)==len(set(required)) and all(isinstance(x,str) for x in required),
            'unique required capabilities must be declared')
    require(set(required)<=set(policy['capabilities']),'capability unavailable in selected profile')
    expected=catalogue['image_repository']+':'+bare+suffix
    config=jsonc(inside(root,root/'.devcontainer/devcontainer.json').read_text())
    image=effective_image(root,config,expected)
    require(isinstance(image,str) and re.fullmatch(re.escape(expected)+r'(?:@sha256:[a-f0-9]{64})?',image),
            'effective workspace image differs from declaration')
    return {'image':image,'profile':profile,'capabilities':sorted(required),'qualification':'SOURCE_ONLY'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repository-root',type=Path,default=Path('.'))
    p.add_argument('--catalogue',type=Path,default=Path(__file__).resolve().parents[1]/'.baobab/environment-profiles.json')
    p.add_argument('--github-output',type=Path)
    args=p.parse_args()
    try:
        result=check(args.repository_root,json.loads(args.catalogue.read_text(),object_pairs_hook=unique))
        if args.github_output:
            with args.github_output.open('a') as f: f.write('image='+result['image']+'\n')
        print(json.dumps(result))
    except (ValueError,KeyError,TypeError,AttributeError,OSError,yaml.YAMLError):
        # Configurations can carry credentials. Never echo values or parser bodies.
        print('DEVELOPMENT_ENVIRONMENT_DENIED: check profile capabilities, exact version and effective workspace image',file=sys.stderr)
        raise SystemExit(1)


if __name__=='__main__': main()

