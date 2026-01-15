'use client';
import { HandCoins } from "lucide-react";
import { Button } from "./ui/button";
import { useWallet } from "./walletProvider";

export default function ClaimButton({ pr_id }: { pr_id: number }) {
    const { wallet } = useWallet();
    return (
    <Button variant="outline" className="hover:cursor-pointer" disabled={!wallet}>
        <HandCoins />
        Redeem $5.00
    </Button>
    )
}