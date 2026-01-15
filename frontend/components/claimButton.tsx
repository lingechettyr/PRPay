'use client';
import { HandCoins } from "lucide-react";
import { Button } from "./ui/button";
import { useWallet } from "./walletProvider";

export default function ClaimButton({ pr_id, payout }: { pr_id: number, payout: number }) {
    const { wallet } = useWallet();
    return (
    <Button variant="outline" className="hover:cursor-pointer" disabled={!wallet}>
        <HandCoins />
        Redeem ${payout.toFixed(2)}
    </Button>
    )
}