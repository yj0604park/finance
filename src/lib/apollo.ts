import { ApolloClient, InMemoryCache, createHttpLink, from } from "@apollo/client";
import { onError } from "@apollo/client/link/error";

const graphqlEndpoint = import.meta.env.VITE_GRAPHQL_ENDPOINT || "/money/graphql";

function redirectToLogin() {
  if (typeof window === "undefined") return;
  window.location.assign("/login");
}

function getCsrfToken(): string {
  const match = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);
  return match ? decodeURIComponent(match[1]) : "";
}

const httpLink = createHttpLink({
  uri: graphqlEndpoint,
  credentials: "include",
  fetch: async (uri, options) => {
    const csrfToken = getCsrfToken();
    const response = await fetch(uri as RequestInfo, {
      ...(options as RequestInit),
      credentials: "include",
      headers: {
        ...(options as RequestInit).headers,
        ...(csrfToken ? { "X-CSRFToken": csrfToken } : {}),
      },
    });

    const contentType = response.headers.get("content-type") || "";

    // If Django redirects to login or returns HTML instead of JSON
    if (response.redirected || response.url.includes("/accounts/login")) {
      redirectToLogin();
      return response;
    }

    if (contentType.includes("text/html")) {
      redirectToLogin();
      throw new Error("UNAUTHENTICATED_HTML_RESPONSE");
    }

    return response;
  },
});

const errorLink = onError(({ graphQLErrors, networkError }) => {
  if (
    graphQLErrors?.some(
      (e) => (e.extensions as Record<string, unknown>)?.code === "UNAUTHENTICATED",
    )
  ) {
    redirectToLogin();
    return;
  }

  const statusCode = (networkError as { statusCode?: number })?.statusCode;
  if (statusCode === 401 || statusCode === 403) {
    redirectToLogin();
    return;
  }

  if ((networkError as Error)?.message?.includes?.("UNAUTHENTICATED_HTML_RESPONSE")) {
    redirectToLogin();
  }
});

export const apolloClient = new ApolloClient({
  link: from([errorLink, httpLink]),
  cache: new InMemoryCache({
    typePolicies: {
      Query: {
        fields: {
          retailerRelay: {
            keyArgs: false,
            merge(existing, incoming) {
              if (!existing) return incoming;
              return {
                ...incoming,
                edges: [...(existing.edges || []), ...(incoming.edges || [])],
              };
            },
          },
        },
      },
    },
  }),
});
