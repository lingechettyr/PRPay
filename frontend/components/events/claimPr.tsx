import { Card, CardAction, CardDescription, CardHeader, CardTitle } from "../ui/card";
import ClaimButton from "../claimButton";

export interface ReviewPRProps {
    pr_id: number;
    pr_title: string;
    pr_created_at: string;
    pr_url: string;
}

export default function ClaimPR(){
    return (
        <Card className="w-full bg-green-300/20">
            <CardHeader>
                <CardTitle>PR Title</CardTitle>
                <CardDescription>PR Date</CardDescription>
                <CardAction>
                    <ClaimButton />
                </CardAction>
            </CardHeader>
        </Card>
    )
}