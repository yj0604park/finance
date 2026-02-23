import { useState } from "react";
import { format, parseISO, subMonths } from "date-fns";
import {
  useGetAllTransactionsQuery,
  useGetSimpleAccountListQuery,
} from "@/graphql/generated/graphql";
import { formatCurrency, getDisplayColor } from "@/lib/format";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
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

const PAGE_SIZE = 50;

const CATEGORY_LABELS: Record<string, string> = {
  ETC: "기타",
  FOOD: "식비",
  TRANSPORT: "교통",
  SHOPPING: "쇼핑",
  HEALTH: "건강",
  CULTURE: "문화",
  TRAVEL: "여행",
  EDUCATION: "교육",
  COMMUNICATION: "통신",
  UTILITY: "공과금",
  INCOME: "수입",
  TRANSFER: "이체",
};

export function TransactionsPage() {
  const defaultEndDate = format(new Date(), "yyyy-MM-dd");
  const defaultStartDate = format(subMonths(new Date(), 3), "yyyy-MM-dd");

  const [accountFilter, setAccountFilter] = useState<string>("all");
  const [startDate, setStartDate] = useState<string>(defaultStartDate);
  const [endDate, setEndDate] = useState<string>(defaultEndDate);
  const [cursor, setCursor] = useState<string>("");
  const [cursorStack, setCursorStack] = useState<string[]>([]);

  const { data: accountData } = useGetSimpleAccountListQuery();
  const accounts = accountData?.accountRelay?.edges ?? [];

  const { data, loading, error } = useGetAllTransactionsQuery({
    variables: {
      first: PAGE_SIZE,
      after: cursor,
      accountId: accountFilter === "all" ? null : accountFilter,
      dateGte: startDate || null,
      dateLte: endDate || null,
    },
  });

  const transactions = data?.transactionRelay?.edges ?? [];
  const pageInfo = data?.transactionRelay?.pageInfo;
  const totalCount = data?.transactionRelay?.totalCount ?? 0;

  function handleNext() {
    if (pageInfo?.endCursor) {
      setCursorStack((prev) => [...prev, cursor]);
      setCursor(pageInfo.endCursor ?? "");
    }
  }

  function handlePrev() {
    const stack = [...cursorStack];
    const prev = stack.pop() ?? "";
    setCursorStack(stack);
    setCursor(prev);
  }

  function handleFilterChange() {
    setCursor("");
    setCursorStack([]);
  }

  const currentPage = cursorStack.length + 1;

  if (error) {
    return (
      <div className="rounded-lg border border-destructive/50 bg-destructive/10 p-6 text-destructive">
        Failed to load transactions: {error.message}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold tracking-tight">Transactions</h1>
        <Badge variant="outline">{totalCount} total</Badge>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="flex flex-wrap gap-4 pt-6">
          <div className="w-52">
            <Select
              value={accountFilter}
              onValueChange={(v) => { setAccountFilter(v); handleFilterChange(); }}
            >
              <SelectTrigger>
                <SelectValue placeholder="All Accounts" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Accounts</SelectItem>
                {accounts.map((edge) => (
                  <SelectItem key={edge.node.id} value={edge.node.id}>
                    {edge.node.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div className="flex items-center gap-2">
            <Input
              type="date"
              value={startDate}
              onChange={(e) => { setStartDate(e.target.value); handleFilterChange(); }}
              className="w-40"
            />
            <span className="text-muted-foreground text-sm">~</span>
            <Input
              type="date"
              value={endDate}
              onChange={(e) => { setEndDate(e.target.value); handleFilterChange(); }}
              className="w-40"
            />
          </div>
        </CardContent>
      </Card>

      {/* Table */}
      <Card>
        <CardContent className="p-0">
          {loading ? (
            <div className="space-y-2 p-6">
              {Array.from({ length: 8 }).map((_, i) => (
                <Skeleton key={`skel-${i.toString()}`} className="h-10 w-full" />
              ))}
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Date</TableHead>
                  <TableHead>Account</TableHead>
                  <TableHead>Retailer</TableHead>
                  <TableHead>Category</TableHead>
                  <TableHead className="text-right">Amount</TableHead>
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
                    const currency = tx.account.currency;
                    return (
                      <TableRow key={tx.id}>
                        <TableCell className="text-sm text-muted-foreground whitespace-nowrap">
                          {format(parseISO(tx.date), "yyyy-MM-dd")}
                        </TableCell>
                        <TableCell className="text-sm">
                          <div className="font-medium">{tx.account.name}</div>
                          <div className="text-muted-foreground text-xs">{tx.account.bank.name}</div>
                        </TableCell>
                        <TableCell className="text-sm">
                          {tx.retailer?.name ?? <span className="text-muted-foreground">—</span>}
                        </TableCell>
                        <TableCell>
                          <Badge variant="outline" className="text-xs">
                            {CATEGORY_LABELS[tx.type] ?? tx.type}
                          </Badge>
                        </TableCell>
                        <TableCell className={`text-right font-mono text-sm ${getDisplayColor(tx.amount)}`}>
                          {formatCurrency(tx.amount, currency)}
                        </TableCell>
                        <TableCell className="text-sm text-muted-foreground max-w-48 truncate">
                          {tx.note ?? ""}
                        </TableCell>
                        <TableCell>
                          <div className="flex gap-1">
                            {tx.isInternal && (
                              <Badge variant="secondary" className="text-xs">Internal</Badge>
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

      {/* Pagination */}
      <div className="flex items-center justify-between">
        <span className="text-sm text-muted-foreground">
          Page {currentPage} · {transactions.length} of {totalCount}
        </span>
        <div className="flex gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={handlePrev}
            disabled={cursorStack.length === 0}
          >
            Previous
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={handleNext}
            disabled={!pageInfo?.hasNextPage}
          >
            Next
          </Button>
        </div>
      </div>
    </div>
  );
}
