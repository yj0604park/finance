import { useParams, useNavigate } from "react-router-dom";
import { useGetSalaryFilteredQuery } from "@/graphql/generated/graphql";
import { formatAccountingUSD, toNumber } from "@/lib/format";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
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
import { ArrowLeft } from "lucide-react";
import { Decimal } from "decimal.js";
import { format, parseISO } from "date-fns";
import { useMemo, useState } from "react";
import { SalaryBarChart } from "./salary-bar-chart";

export function IncomeYearDetailPage() {
  const { year } = useParams<{ year: string }>();
  const navigate = useNavigate();
  const [expandedId, setExpandedId] = useState<string | null>(null);

  const dateMin = `${year}-01-01`;
  const dateMax = `${year}-12-31`;

  const { data, loading } = useGetSalaryFilteredQuery({
    variables: { dateMin, dateMax },
    skip: !year,
  });

  const salaries = data?.salaryRelay?.edges ?? [];

  // Totals
  const totals = useMemo(() => {
    let grossPay = new Decimal(0);
    let adjustment = new Decimal(0);
    let withheld = new Decimal(0);
    let deduction = new Decimal(0);
    let netPay = new Decimal(0);

    for (const edge of salaries) {
      const s = edge.node;
      grossPay = grossPay.plus(new Decimal(s.grossPay || 0));
      adjustment = adjustment.plus(new Decimal(s.totalAdjustment || 0));
      withheld = withheld.plus(new Decimal(s.totalWithheld || 0));
      deduction = deduction.plus(new Decimal(s.totalDeduction || 0));
      netPay = netPay.plus(new Decimal(s.netPay || 0));
    }

    return { grossPay, adjustment, withheld, deduction, netPay };
  }, [salaries]);

  // Chart data
  const chartData = salaries.map((edge) => ({
    date: edge.node.date,
    grossPay: toNumber(edge.node.grossPay),
    netPay: toNumber(edge.node.netPay),
  }));

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon" onClick={() => navigate("/income")}>
          <ArrowLeft className="h-4 w-4" />
        </Button>
        <h1 className="text-3xl font-bold tracking-tight">Income {year}</h1>
        <Badge variant="outline">{salaries.length} pay periods</Badge>
      </div>

      {/* Summary Cards */}
      {!loading && (
        <div className="grid gap-4 md:grid-cols-3 lg:grid-cols-5">
          <SummaryCard title="Gross Pay" value={totals.grossPay.toString()} />
          <SummaryCard title="Adjustments" value={totals.adjustment.toString()} negative />
          <SummaryCard title="Withheld" value={totals.withheld.toString()} negative />
          <SummaryCard title="Deductions" value={totals.deduction.toString()} negative />
          <SummaryCard title="Net Pay" value={totals.netPay.toString()} />
        </div>
      )}

      {/* Chart */}
      <SalaryBarChart data={chartData} loading={loading} />

      {/* Detail Table */}
      <Card>
        <CardHeader>
          <CardTitle>Pay Periods</CardTitle>
        </CardHeader>
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
                  <TableHead>Date</TableHead>
                  <TableHead className="text-right">Gross Pay</TableHead>
                  <TableHead className="text-right">Adjustments</TableHead>
                  <TableHead className="text-right">Withheld</TableHead>
                  <TableHead className="text-right">Deductions</TableHead>
                  <TableHead className="text-right">Net Pay</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {salaries.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={6} className="text-center text-muted-foreground py-8">
                      No salary data for {year}
                    </TableCell>
                  </TableRow>
                ) : (
                  <>
                    {salaries.map((edge) => {
                      const s = edge.node;
                      const isExpanded = expandedId === s.id;
                      return (
                        <TableRow
                          key={s.id}
                          className="cursor-pointer hover:bg-muted/50"
                          onClick={() => setExpandedId(isExpanded ? null : s.id)}
                        >
                          <TableCell className="font-medium">
                            {formatDateSafe(s.date)}
                          </TableCell>
                          <TableCell className="text-right font-mono">
                            {formatAccountingUSD(s.grossPay)}
                          </TableCell>
                          <TableCell className="text-right font-mono text-red-600">
                            {formatAccountingUSD(s.totalAdjustment)}
                          </TableCell>
                          <TableCell className="text-right font-mono text-red-600">
                            {formatAccountingUSD(s.totalWithheld)}
                          </TableCell>
                          <TableCell className="text-right font-mono text-red-600">
                            {formatAccountingUSD(s.totalDeduction)}
                          </TableCell>
                          <TableCell className="text-right font-mono font-semibold">
                            {formatAccountingUSD(s.netPay)}
                          </TableCell>
                        </TableRow>
                      );
                    })}
                    {/* Totals Row */}
                    <TableRow className="bg-muted/50 font-semibold">
                      <TableCell>Total</TableCell>
                      <TableCell className="text-right font-mono">
                        {formatAccountingUSD(totals.grossPay.toString())}
                      </TableCell>
                      <TableCell className="text-right font-mono text-red-600">
                        {formatAccountingUSD(totals.adjustment.toString())}
                      </TableCell>
                      <TableCell className="text-right font-mono text-red-600">
                        {formatAccountingUSD(totals.withheld.toString())}
                      </TableCell>
                      <TableCell className="text-right font-mono text-red-600">
                        {formatAccountingUSD(totals.deduction.toString())}
                      </TableCell>
                      <TableCell className="text-right font-mono">
                        {formatAccountingUSD(totals.netPay.toString())}
                      </TableCell>
                    </TableRow>
                  </>
                )}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

function SummaryCard({ title, value, negative }: { title: string; value: string; negative?: boolean }) {
  return (
    <Card>
      <CardHeader className="pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground">{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <p className={`text-xl font-bold font-mono ${negative ? "text-red-600" : ""}`}>
          {formatAccountingUSD(value)}
        </p>
      </CardContent>
    </Card>
  );
}

function formatDateSafe(dateStr: string): string {
  try {
    return format(parseISO(dateStr), "yyyy-MM-dd");
  } catch {
    return dateStr;
  }
}
