import { useState } from "react";
import {
  useCreateTransactionMutation,
  useCreateTransactionWithoutRetailerMutation,
  useGetRetailerListQuery,
} from "@/graphql/generated/graphql";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { toast } from "sonner";

interface CreateTransactionDialogProps {
  accountId: string;
  currency: string;
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSuccess: () => void;
}

export function CreateTransactionDialog({
  accountId,
  currency,
  open,
  onOpenChange,
  onSuccess,
}: CreateTransactionDialogProps) {
  const [amount, setAmount] = useState("");
  const [date, setDate] = useState("");
  const [note, setNote] = useState("");
  const [retailerId, setRetailerId] = useState<string>("none");
  const [isInternal, setIsInternal] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const { data: retailerData } = useGetRetailerListQuery();
  const retailers = retailerData?.retailerRelay?.edges ?? [];

  const [createTransaction] = useCreateTransactionMutation();
  const [createTransactionWithoutRetailer] = useCreateTransactionWithoutRetailerMutation();

  async function handleSubmit() {
    if (!amount || !date) {
      toast.error("Amount and date are required");
      return;
    }

    setSubmitting(true);
    try {
      if (isInternal || retailerId === "none") {
        await createTransactionWithoutRetailer({
          variables: {
            amount,
            date,
            accountId,
            isInternal,
            note: note || null,
          },
        });
      } else {
        await createTransaction({
          variables: {
            amount,
            date,
            accountId,
            isInternal: false,
            note: note || null,
            retailerId,
          },
        });
      }
      toast.success("Transaction created");
      onSuccess();
    } catch (err) {
      toast.error(`Failed to create transaction: ${err instanceof Error ? err.message : "Unknown error"}`);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[480px]">
        <DialogHeader>
          <DialogTitle>Create Transaction</DialogTitle>
          <DialogDescription>
            Add a new transaction to this account ({currency}).
          </DialogDescription>
        </DialogHeader>

        <div className="grid gap-4 py-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="amount">Amount</Label>
              <Input
                id="amount"
                type="number"
                step="0.01"
                placeholder="0.00"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="date">Date</Label>
              <Input
                id="date"
                type="date"
                value={date}
                onChange={(e) => setDate(e.target.value)}
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="retailer">Retailer</Label>
            <Select
              value={retailerId}
              onValueChange={setRetailerId}
              disabled={isInternal}
            >
              <SelectTrigger>
                <SelectValue placeholder="Select retailer" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="none">No retailer</SelectItem>
                {retailers.map((edge) => (
                  <SelectItem key={edge.node.id} value={edge.node.id}>
                    {edge.node.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="note">Note</Label>
            <Input
              id="note"
              placeholder="Optional note"
              value={note}
              onChange={(e) => setNote(e.target.value)}
            />
          </div>

          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              id="isInternal"
              checked={isInternal}
              onChange={(e) => {
                setIsInternal(e.target.checked);
                if (e.target.checked) setRetailerId("none");
              }}
              className="h-4 w-4 rounded border-input"
            />
            <Label htmlFor="isInternal" className="text-sm">
              Internal transfer
            </Label>
          </div>
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={() => onOpenChange(false)} disabled={submitting}>
            Cancel
          </Button>
          <Button onClick={handleSubmit} disabled={submitting}>
            {submitting ? "Creating..." : "Create"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
