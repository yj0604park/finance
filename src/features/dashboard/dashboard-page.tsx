import { useGetBankListQuery, useGetAmountSnapshotsQuery } from "@/graphql/generated/graphql";
import { formatCurrency, getTotalBalance } from "@/lib/format";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { Badge } from "@/components/ui/badge";
import { BalanceChart } from "./balance-chart";
import { BankCard } from "./bank-card";

export function DashboardPage() {
  const { data, loading, error } = useGetBankListQuery();
  const { data: snapshotData, loading: snapshotLoading } = useGetAmountSnapshotsQuery({
    variables: { startDate: null },
  });

  if (error) {
    return (
      <div className="rounded-lg border border-destructive/50 bg-destructive/10 p-6 text-destructive">
        Failed to load dashboard data: {error.message}
      </div>
    );
  }

  const banks = data?.bankRelay?.edges ?? [];
  const krwTotal = banks.length > 0 ? getTotalBalance(banks, "KRW") : "0";
  const usdTotal = banks.length > 0 ? getTotalBalance(banks, "USD") : "0";

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>

      {/* Balance Summary */}
      <div className="grid gap-4 md:grid-cols-2">
        <BalanceSummaryCard
          title="Total Balance (KRW)"
          amount={krwTotal}
          currency="KRW"
          loading={loading}
        />
        <BalanceSummaryCard
          title="Total Balance (USD)"
          amount={usdTotal}
          currency="USD"
          loading={loading}
        />
      </div>

      {/* Balance Charts */}
      <div className="grid gap-4 md:grid-cols-2">
        <BalanceChart
          title="KRW Balance Trend"
          data={snapshotData?.krwSnapshot?.edges ?? []}
          loading={snapshotLoading}
          currency="KRW"
        />
        <BalanceChart
          title="USD Balance Trend"
          data={snapshotData?.usdSnapshot?.edges ?? []}
          loading={snapshotLoading}
          currency="USD"
        />
      </div>

      {/* Bank List */}
      <div>
        <h2 className="mb-4 text-xl font-semibold">Banks</h2>
        {loading ? (
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {Array.from({ length: 4 }).map((_, i) => (
              <Skeleton key={`skel-${i.toString()}`} className="h-32" />
            ))}
          </div>
        ) : (
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {banks.map((bank) => (
              <BankCard key={bank.node.id} bank={bank.node} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

function BalanceSummaryCard({
  title,
  amount,
  currency,
  loading,
}: {
  title: string;
  amount: string;
  currency: string;
  loading: boolean;
}) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        <Badge variant="outline">{currency}</Badge>
      </CardHeader>
      <CardContent>
        {loading ? (
          <Skeleton className="h-8 w-48" />
        ) : (
          <div className="text-2xl font-bold">{formatCurrency(amount, currency)}</div>
        )}
      </CardContent>
    </Card>
  );
}
