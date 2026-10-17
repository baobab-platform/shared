"use client";

import type {ReactNode} from "react";
import {Dialog as BaseDialog} from "@base-ui/react/dialog";
import {Tabs as BaseTabs} from "@base-ui/react/tabs";

/**
 * Neutral controlled modal. The trigger remains inside the same Base UI root
 * so focus restoration, Escape and portal isolation share one lifecycle.
 * Closing a modal only requests a UI state change; consequential commands and
 * receipts belong to the caller's authorised application workflow.
 */
export function ExperienceDialog({open,onOpenChange,trigger,title,description,children}:Readonly<{
  open:boolean;onOpenChange:(open:boolean)=>void;trigger:ReactNode;
  title:string;description?:string;children:ReactNode;
}>){
  return <BaseDialog.Root open={open} onOpenChange={onOpenChange}>
    <BaseDialog.Trigger className="bx-button bx-button--secondary">{trigger}</BaseDialog.Trigger>
    <BaseDialog.Portal>
      <BaseDialog.Backdrop className="bx-dialog-backdrop"/>
      <BaseDialog.Popup className="bx-dialog">
        <BaseDialog.Title>{title}</BaseDialog.Title>
        {description?<BaseDialog.Description>{description}</BaseDialog.Description>:null}
        {children}
        <BaseDialog.Close className="bx-button bx-button--secondary">Close</BaseDialog.Close>
      </BaseDialog.Popup>
    </BaseDialog.Portal>
  </BaseDialog.Root>;
}

export type ExperienceTab=Readonly<{id:string;label:string;content:ReactNode}>;
/**
 * Base UI owns roving focus and direction-aware keyboard navigation. Tabs
 * select previously-authorised views; they never grant access to hidden data.
 */
export function ExperienceTabs({label,items,initialTab}:Readonly<{
  label:string;items:readonly ExperienceTab[];initialTab?:string;
}>){
  const ids=new Set<string>();
  for(const item of items){
    if(!item.id.trim()||ids.has(item.id)||!item.label.trim())throw new TypeError("Tabs require unique IDs and readable labels");
    ids.add(item.id);
  }
  if(initialTab!==undefined&&!ids.has(initialTab))throw new TypeError("Unknown initial tab");
  return <BaseTabs.Root defaultValue={initialTab??items[0]?.id} className="bx-tabs">
    <BaseTabs.List aria-label={label}>{items.map(item=><BaseTabs.Tab key={item.id} value={item.id}>{item.label}</BaseTabs.Tab>)}</BaseTabs.List>
    {items.map(item=><BaseTabs.Panel key={item.id} value={item.id}>{item.content}</BaseTabs.Panel>)}
  </BaseTabs.Root>;
}
