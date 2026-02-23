import { ApolloProvider } from "@apollo/client";
import { BrowserRouter, useRoutes } from "react-router-dom";
import { Toaster } from "@/components/ui/sonner";
import { ErrorBoundary } from "@/components/shared/error-boundary";
import { AuthProvider } from "@/providers/auth-provider";
import { apolloClient } from "@/lib/apollo";
import { routes } from "@/routes";

function AppRoutes() {
  return useRoutes(routes);
}

export default function App() {
  return (
    <ErrorBoundary>
      <ApolloProvider client={apolloClient}>
        <BrowserRouter>
          <AuthProvider>
            <AppRoutes />
            <Toaster />
          </AuthProvider>
        </BrowserRouter>
      </ApolloProvider>
    </ErrorBoundary>
  );
}
