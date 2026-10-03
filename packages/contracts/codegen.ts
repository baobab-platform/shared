// Points at every .graphql file under graphql/ — currently just the
// placeholder health schema. Real product subgraph schemas (Trade
// Intelligence, Property Intelligence, BIE) will be added under this same
// directory once they exist; no config change should be needed for that.
const config = {
  schema: 'graphql/**/*.graphql',
  generates: {
    'src/generated/graphql.ts': {
      plugins: ['typescript'],
    },
  },
};

export default config;
