import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useGetAccountListQuery, useGetBankSimpleListQuery } from "@/graphql/generated/graphql";
import { formatCurrency, getDisplayColor } from "@/lib/format";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { format, parseISO } from "date-fns";

const ACCOUNT_TYPE_LABELS: Record<string, string> = {
  CHECKING_ACCOUNT: "Checking",
  SAVINGS_ACCOUNT: "Savings",
  INSTALLMENT_SAVING: "Installment",
  TIME_DEPOSIT: "Time Deposit",
  CREDIT_CARD: "Credit Card",
  STOCK: "Stock",
  LOAN: "Loan",
};

export function AccountsPage() {
  const [bankFilter, setBankFilter] = useState<string>("all");
  const [activeFilter, setActiveFilter] = useState<string>("active");

  const { data: bankData } = useGetBankSimpleListQuery();

  const isActiveFilter =
    activeFilter === "all"
      ? null
      : { exact: activeFilter === "active", inList: null, isNull: null };

  const { data, loading, error } = useGetAccountListQuery({
    variables: {
      after: "",
      bankId: bankFilter === "all" ? null : bankFilter,
      isActive: isActiveFilter,
    },
  });

  const navigate = useNavigate();
  const accounts = data?.accountRelay?.edges ?? [];
  const banks = bankData?.bankRelay?.edges ?? [];

  if (error) {
    return (
      <div className="rounded-lg border border-destructive/50 bg-destructive/10 p-6 text-destructive">
        Failed to load accounts: {error.message}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold tracking-tight">Accounts</h1>
        <Badge variant="outline">{data?.accountRelay?.totalCount ?? 0} total</Badge>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="flex gap-4 pt-6">
          <div className="w-48">
            <Select value={bankFilter} onValueChange={setBankFilter}>
              <SelectTrigger>
                <SelectValue placeholder="All Banks" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Banks</SelectItem>
                {banks.map((bank) => (
                  <SelectItem key={bank.node.id} value={bank.node.id}>
                    {bank.node.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div className="w-40">
            <Select value={activeFilter} onValueChange={setActiveFilter}>
              <SelectTrigger>
                <SelectValue placeholder="Status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All</SelectItem>
                <SelectItem value="active">Active</SelectItem>
                <SelectItem value="inactive">Inactive</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Account Table */}
      <Card>
        <CardContent className="p-0">
          {loading ? (
            <div className="space-y-2 p-6">
              {Array.from({ length: 5 }).map((_, i) => (
                <Skeleton key={`skel-${i.toString()}`} className="h-10 w-full" />
              ))}
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Name</TableHead>
                  <TableHead>Bank</TableHead>
                  <TableHead>Type</TableHead>
                  <TableHead>Currency</TableHead>
                  <TableHead className="text-right">Balance</TableHead>
                  <TableHead>First Txn</TableHead>
                  <TableHead>Last Txn</TableHead>
                  <TableHead>Status</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {accounts.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={8} className="text-center text-muted-foreground py-8">
                      No accounts found
                    </TableCell>
                  </TableRow>
                ) : (
                  accounts.map((edge) => {
                    const account = edge.node;
                    return (
                      <TableRow
                        key={account.id}
                        className="cursor-pointer hover:bg-muted/50"
                        onClick={() => navigate(`/accounts/${encodeURIComponent(account.id)}`)}
                      >
                        <TableCell className="font-medium">{account.name}</TableCell>
                        <TableCell>{account.bank.name}</TableCell>
                        <TableCell>
                          <Badge variant="outline" className="text-xs">
                            {ACCOUNT_TYPE_LABELS[account.type] || account.type}
                          </Badge>
                        </TableCell>
                        <TableCell>{account.currency}</TableCell>
                        <TableCell className={`text-right font-mono ${getDisplayColor(account.amount)}`}>
                          {formatCurrency(account.amount, account.currency)}
                        </TableCell>
                        <TableCell className="text-muted-foreground text-sm">
                          {account.firstTransaction ? formatDate(account.firstTransaction) : "—"}
                        </TableCell>
                        <TableCell className="text-muted-foreground text-sm">
                          {account.lastTransaction ? formatDate(account.lastTransaction) : "—"}
                        </TableCell>
                        <TableCell>
                          <Badge variant={account.isActive ? "default" : "secondary"}>
                            {account.isActive ? "Active" : "Inactive"}
                          </Badge>
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
    </div>
  );
}

function formatDate(dateStr: string): string {
  try {
    return format(parseISO(dateStr), "yyyy-MM-dd");
  } catch {
    return dateStr;
  }
}
