import { useNavigate } from "react-router-dom";
import { useGetSalaryListQuery } from "@/graphql/generated/graphql";
import { formatAccountingUSD, toNumber } from "@/lib/format";
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
import { Decimal } from "decimal.js";
import { SalaryBarChart } from "./salary-bar-chart";

interface YearSummary {
  year: number;
  grossPay: Decimal;
  adjustment: Decimal;
  withheld: Decimal;
  deduction: Decimal;
  netPay: Decimal;
}

export function IncomePage() {
  const { data: salaryData, loading: salaryLoading } = useGetSalaryListQuery();

  const loading = salaryLoading;
  const salaries = salaryData?.salaryRelay?.edges ?? [];

  // Aggregate by year
  const yearMap = new Map<number, YearSummary>();
  for (const edge of salaries) {
    const s = edge.node;
    const year = new Date(s.date).getFullYear();
    if (!yearMap.has(year)) {
      yearMap.set(year, {
        year,
        grossPay: new Decimal(0),
        adjustment: new Decimal(0),
        withheld: new Decimal(0),
        deduction: new Decimal(0),
        netPay: new Decimal(0),
      });
    }
    const summary = yearMap.get(year)!;
    summary.grossPay = summary.grossPay.plus(new Decimal(s.grossPay || 0));
    summary.adjustment = summary.adjustment.plus(new Decimal(s.totalAdjustment || 0));
    summary.withheld = summary.withheld.plus(new Decimal(s.totalWithheld || 0));
    summary.deduction = summary.deduction.plus(new Decimal(s.totalDeduction || 0));
    summary.netPay = summary.netPay.plus(new Decimal(s.netPay || 0));
  }

  const yearSummaries = Array.from(yearMap.values()).sort((a, b) => b.year - a.year);

  const navigate = useNavigate();

  // Chart data
  const chartData = salaries.map((edge) => ({
    date: edge.node.date,
    grossPay: toNumber(edge.node.grossPay),
    netPay: toNumber(edge.node.netPay),
  }));

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold tracking-tight">Income</h1>

      {/* Salary Chart */}
      <SalaryBarChart data={chartData} loading={loading} />

      {/* Year Summary Table */}
      <Card>
        <CardHeader>
          <CardTitle>Yearly Summary</CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          {loading ? (
            <div className="space-y-2 p-6">
              {Array.from({ length: 3 }).map((_, i) => (
                <Skeleton key={`skel-${i.toString()}`} className="h-10 w-full" />
              ))}
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Year</TableHead>
                  <TableHead className="text-right">Gross Pay</TableHead>
                  <TableHead className="text-right">Adjustments</TableHead>
                  <TableHead className="text-right">Withheld</TableHead>
                  <TableHead className="text-right">Deductions</TableHead>
                  <TableHead className="text-right">Net Pay</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {yearSummaries.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={6} className="text-center text-muted-foreground py-8">
                      No salary data found
                    </TableCell>
                  </TableRow>
                ) : (
                  yearSummaries.map((summary) => (
                    <TableRow
                      key={summary.year}
                      className="cursor-pointer hover:bg-muted/50"
                      onClick={() => navigate(`/income/${summary.year}`)}
                    >
                      <TableCell className="font-medium">{summary.year}</TableCell>
                      <TableCell className="text-right font-mono">
                        {formatAccountingUSD(summary.grossPay.toString())}
                      </TableCell>
                      <TableCell className="text-right font-mono text-red-600">
                        {formatAccountingUSD(summary.adjustment.toString())}
                      </TableCell>
                      <TableCell className="text-right font-mono text-red-600">
                        {formatAccountingUSD(summary.withheld.toString())}
                      </TableCell>
                      <TableCell className="text-right font-mono text-red-600">
                        {formatAccountingUSD(summary.deduction.toString())}
                      </TableCell>
                      <TableCell className="text-right font-mono font-semibold">
                        {formatAccountingUSD(summary.netPay.toString())}
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
