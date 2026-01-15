'use client';
import { HandCoins } from "lucide-react";
import { Button } from "./ui/button";
import { useWallet } from "./walletProvider";
import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase/client";

export default function ClaimButton({ pr_id, payout }: { pr_id: number, payout: number }) {
    const [githubId, setGithubId] = useState<string | null>(null);
    const [claimed, setClaimed] = useState(false);
    const { wallet } = useWallet();
    useEffect(() => {
        async function getUser(){
            const {data: { user }} = await supabase.auth.getUser();
            const githubId = user?.user_metadata?.provider_id || null;
            setGithubId(githubId);
        }
        getUser();
    }, []);

    const handleClaim = async () => {
        const res = await fetch(
            `${process.env.NEXT_PUBLIC_BACKEND_URL}/claimPr`,
            {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: githubId,
                pr_id: pr_id
            })
            }
        );

        const data = await res.json();
        console.log('Claim response:', data);
        if(data.success){
            setClaimed(true);
        }
    }

    return (
    <Button variant="outline" className="hover:cursor-pointer" disabled={!wallet || !githubId || claimed} onClick={handleClaim}>
        <HandCoins />
        {!claimed ? `Redeem ${payout.toFixed(2)}` : "Claimed"}
    </Button>
    )
}