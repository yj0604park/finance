import { useParams, useNavigate } from "react-router-dom";
import { useGetAccountDetailQuery, useGetTransactionListQuery } from "@/graphql/generated/graphql";
import { formatCurrency, getDisplayColor } from "@/lib/format";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { ArrowLeft, Plus } from "lucide-react";
import { format, parseISO } from "date-fns";
import { useState } from "react";
import { CreateTransactionDialog } from "@/features/transactions/create-transaction-dialog";

const ACCOUNT_TYPE_LABELS: Record<string, string> = {
  CHECKING_ACCOUNT: "Checking",
  SAVINGS_ACCOUNT: "Savings",
  INSTALLMENT_SAVING: "Installment",
  TIME_DEPOSIT: "Time Deposit",
  CREDIT_CARD: "Credit Card",
  STOCK: "Stock",
  LOAN: "Loan",
};

export function AccountDetailPage() {
  const { accountId } = useParams<{ accountId: string }>();
  const navigate = useNavigate();
  const [showCreateDialog, setShowCreateDialog] = useState(false);

  const decodedId = accountId ? decodeURIComponent(accountId) : undefined;

  const { data: accountData, loading: accountLoading } = useGetAccountDetailQuery({
    variables: { accountId: decodedId ?? null },
    skip: !decodedId,
  });

  const {
    data: txData,
    loading: txLoading,
    refetch: refetchTransactions,
  } = useGetTransactionListQuery({
    variables: { accountId: decodedId ?? null },
    skip: !decodedId,
  });

  const account = accountData?.accountRelay?.edges?.[0]?.node;
  const transactions = txData?.transactionRelay?.edges ?? [];
  const currency = txData?.accountRelay?.edges?.[0]?.node?.currency ?? account?.currency ?? "KRW";

  if (!decodedId) {
    return (
      <div className="flex h-64 items-center justify-center text-muted-foreground">
        No account selected. Please select an account from the accounts list.
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon" onClick={() => navigate("/accounts")}>
          <ArrowLeft className="h-4 w-4" />
        </Button>
        {accountLoading ? (
          <Skeleton className="h-8 w-64" />
        ) : (
          <div className="flex items-center gap-3">
            <h1 className="text-3xl font-bold tracking-tight">{account?.name ?? "Account"}</h1>
            {account && (
              <>
                <Badge variant="outline">{account.bank.name}</Badge>
                <Badge variant="secondary">
                  {ACCOUNT_TYPE_LABELS[account.type] || account.type}
                </Badge>
              </>
            )}
          </div>
        )}
      </div>

      {/* Account Summary */}
      {account && (
        <div className="grid gap-4 md:grid-cols-3">
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">Balance</CardTitle>
            </CardHeader>
            <CardContent>
              <p className={`text-2xl font-bold ${getDisplayColor(account.amount)}`}>
                {formatCurrency(account.amount, account.currency)}
              </p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Transaction Period
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm">
                {account.firstTransaction ?? "—"} ~ {account.lastTransaction ?? "—"}
              </p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Total Transactions
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-2xl font-bold">{txData?.transactionRelay?.totalCount ?? "—"}</p>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Transactions */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle>Transactions</CardTitle>
          <Button size="sm" onClick={() => setShowCreateDialog(true)}>
            <Plus className="mr-1 h-4 w-4" />
            Add Transaction
          </Button>
        </CardHeader>
        <CardContent className="p-0">
          {txLoading ? (
            <div className="space-y-2 p-6">
              {Array.from({ length: 5 }).map((_, i) => (
                <Skeleton key={`skel-${i.toString()}`} className="h-10 w-full" />
              ))}
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Date</TableHead>
                  <TableHead>Retailer</TableHead>
                  <TableHead>Category</TableHead>
                  <TableHead className="text-right">Amount</TableHead>
                  <TableHead className="text-right">Balance</TableHead>
                  <TableHead>Note</TableHead>
                  <TableHead>Flags</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {transactions.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={7} className="text-center text-muted-foreground py-8">
                      No transactions found
                    </TableCell>
                  </TableRow>
                ) : (
                  transactions.map((edge) => {
                    const tx = edge.node;
                    return (
                      <TableRow key={tx.id}>
                        <TableCell className="text-sm">
                          {formatDateSafe(tx.date)}
                        </TableCell>
                        <TableCell>{tx.retailer?.name ?? "—"}</TableCell>
                        <TableCell>
                          <Badge variant="outline" className="text-xs">
                            {tx.type}
                          </Badge>
                        </TableCell>
                        <TableCell className={`text-right font-mono ${getDisplayColor(tx.amount)}`}>
                          {formatCurrency(tx.amount, currency)}
                        </TableCell>
                        <TableCell className="text-right font-mono text-muted-foreground">
                          {tx.balance ? formatCurrency(tx.balance, currency) : "—"}
                        </TableCell>
                        <TableCell className="max-w-[200px] truncate text-sm text-muted-foreground">
                          {tx.note || "—"}
                        </TableCell>
                        <TableCell>
                          <div className="flex gap-1">
                            {tx.isInternal && (
                              <Badge variant="secondary" className="text-xs">
                                Internal
                              </Badge>
                            )}
                            {tx.reviewed && (
                              <Badge variant="default" className="text-xs">
                                Reviewed
                              </Badge>
                            )}
                          </div>
                        </TableCell>
                      </TableRow>
                    );
                  })
                )}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>

      {showCreateDialog && decodedId && (
        <CreateTransactionDialog
          accountId={decodedId}
          currency={currency}
          open={showCreateDialog}
          onOpenChange={setShowCreateDialog}
          onSuccess={() => {
            refetchTransactions();
            setShowCreateDialog(false);
          }}
        />
      )}
    </div>
  );
}

function formatDateSafe(dateStr: string): string {
  try {
    return format(parseISO(dateStr), "yyyy-MM-dd");
  } catch {
    return dateStr;
  }
}
