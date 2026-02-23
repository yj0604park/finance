import { useGetStockListQuery } from "@/graphql/generated/graphql";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

export function StocksPage() {
  const { data, loading, error } = useGetStockListQuery();
  const stocks = data?.stockRelay?.edges ?? [];

  if (error) {
    return (
      <div className="rounded-lg border border-destructive/50 bg-destructive/10 p-6 text-destructive">
        Failed to load stocks: {error.message}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold tracking-tight">Stocks</h1>
        <Badge variant="outline">{data?.stockRelay?.totalCount ?? 0} positions</Badge>
      </div>

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
                  <TableHead>Ticker</TableHead>
                  <TableHead>Name</TableHead>
                  <TableHead>Currency</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {stocks.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={3} className="text-center text-muted-foreground py-8">
                      No stocks found
                    </TableCell>
                  </TableRow>
                ) : (
                  stocks.map((edge) => {
                    const stock = edge.node;
                    return (
                      <TableRow key={stock.id}>
                        <TableCell className="font-mono font-medium">
                          {stock.ticker ?? "—"}
                        </TableCell>
                        <TableCell>{stock.name}</TableCell>
                        <TableCell>
                          <Badge variant="outline">{stock.currency}</Badge>
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
