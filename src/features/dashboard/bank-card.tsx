import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { formatCurrency } from "@/lib/format";
import { Building2 } from "lucide-react";

interface BankBalance {
  currency: string;
  value: string;
}

interface BankCardProps {
  bank: {
    id: string;
    name: string;
    balance: ReadonlyArray<BankBalance>;
    accountSet: {
      totalCount: number | null;
    };
  };
}

export function BankCard({ bank }: BankCardProps) {
  return (
    <Card className="transition-colors hover:bg-muted/50">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium flex items-center gap-2">
          <Building2 className="h-4 w-4 text-muted-foreground" />
          {bank.name}
        </CardTitle>
        <Badge variant="secondary" className="text-xs">
          {bank.accountSet.totalCount ?? 0} accounts
        </Badge>
      </CardHeader>
      <CardContent className="space-y-1">
        {bank.balance.map((b) => (
          <div key={b.currency} className="flex items-center justify-between">
            <span className="text-xs text-muted-foreground">{b.currency}</span>
            <span className="text-sm font-semibold">{formatCurrency(b.value, b.currency)}</span>
          </div>
        ))}
        {bank.balance.length === 0 && (
          <p className="text-xs text-muted-foreground">No balance data</p>
        )}
      </CardContent>
    </Card>
  );
}
