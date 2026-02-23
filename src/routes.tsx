import { lazy, Suspense } from "react";
import { Navigate, type RouteObject } from "react-router-dom";
import { AuthGuard } from "@/components/shared/auth-guard";
import { AppShell } from "@/components/layout/app-shell";

// Lazy-loaded pages
const LoginPage = lazy(() =>
  import("@/features/auth/login-page").then((m) => ({ default: m.LoginPage })),
);
const DashboardPage = lazy(() =>
  import("@/features/dashboard/dashboard-page").then((m) => ({ default: m.DashboardPage })),
);
const AccountsPage = lazy(() =>
  import("@/features/accounts/accounts-page").then((m) => ({ default: m.AccountsPage })),
);
const AccountDetailPage = lazy(() =>
  import("@/features/accounts/account-detail-page").then((m) => ({
    default: m.AccountDetailPage,
  })),
);
const IncomePage = lazy(() =>
  import("@/features/income/income-page").then((m) => ({ default: m.IncomePage })),
);
const IncomeYearDetailPage = lazy(() =>
  import("@/features/income/income-year-detail-page").then((m) => ({
    default: m.IncomeYearDetailPage,
  })),
);
const TransactionsPage = lazy(() =>
  import("@/features/transactions/transactions-page").then((m) => ({
    default: m.TransactionsPage,
  })),
);
const CategoryPage = lazy(() =>
  import("@/features/transactions/category-page").then((m) => ({ default: m.CategoryPage })),
);
const RetailersPage = lazy(() =>
  import("@/features/retailers/retailers-page").then((m) => ({ default: m.RetailersPage })),
);
const StocksPage = lazy(() =>
  import("@/features/stocks/stocks-page").then((m) => ({ default: m.StocksPage })),
);

function SuspenseWrapper({ children }: { children: React.ReactNode }) {
  return (
    <Suspense
      fallback={
        <div className="flex h-full items-center justify-center">
          <div className="text-muted-foreground">Loading...</div>
        </div>
      }
    >
      {children}
    </Suspense>
  );
}

export const routes: RouteObject[] = [
  {
    path: "/login",
    element: (
      <SuspenseWrapper>
        <LoginPage />
      </SuspenseWrapper>
    ),
  },
  {
    path: "/",
    element: (
      <AuthGuard>
        <AppShell />
      </AuthGuard>
    ),
    children: [
      { index: true, element: <Navigate to="/dashboard" replace /> },
      {
        path: "dashboard",
        element: (
          <SuspenseWrapper>
            <DashboardPage />
          </SuspenseWrapper>
        ),
      },
      {
        path: "accounts",
        element: (
          <SuspenseWrapper>
            <AccountsPage />
          </SuspenseWrapper>
        ),
      },
      {
        path: "accounts/:accountId",
        element: (
          <SuspenseWrapper>
            <AccountDetailPage />
          </SuspenseWrapper>
        ),
      },
      {
        path: "transactions",
        element: (
          <SuspenseWrapper>
            <TransactionsPage />
          </SuspenseWrapper>
        ),
      },
      {
        path: "categories",
        element: (
          <SuspenseWrapper>
            <CategoryPage />
          </SuspenseWrapper>
        ),
      },
      {
        path: "retailers",
        element: (
          <SuspenseWrapper>
            <RetailersPage />
          </SuspenseWrapper>
        ),
      },
      {
        path: "income",
        element: (
          <SuspenseWrapper>
            <IncomePage />
          </SuspenseWrapper>
        ),
      },
      {
        path: "income/:year",
        element: (
          <SuspenseWrapper>
            <IncomeYearDetailPage />
          </SuspenseWrapper>
        ),
      },
      {
        path: "stocks",
        element: (
          <SuspenseWrapper>
            <StocksPage />
          </SuspenseWrapper>
        ),
      },
    ],
  },
  {
    path: "*",
    element: <Navigate to="/dashboard" replace />,
  },
];
