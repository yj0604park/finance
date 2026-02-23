import type { CodegenConfig } from "@graphql-codegen/cli";

const config: CodegenConfig = {
  schema: "../backend/schema.graphql",
  documents: "src/graphql/**/*.graphql",
  generates: {
    "src/graphql/generated/graphql.ts": {
      plugins: [
        "typescript",
        "typescript-operations",
        "typescript-react-apollo",
      ],
      config: {
        withHooks: true,
        withComponent: false,
        avoidOptionals: true,
        scalars: {
          Date: "string",
          DateTime: "string",
          Decimal: "string",
          UUID: "string",
          JSON: "Record<string, unknown>",
          GlobalID: "string",
        },
      },
    },
  },
};

export default config;
