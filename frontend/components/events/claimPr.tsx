import { Card, CardAction, CardDescription, CardHeader, CardTitle } from "../ui/card";
import ClaimButton from "../claimButton";
import ReviewPRProps from "./types";

export default function ClaimPR(props: ReviewPRProps){
    return (
        <Card className="w-full bg-green-300/20">
            <CardHeader>
                <CardTitle>{props.pr_title}</CardTitle>
                <CardDescription>{props.pr_created_at}</CardDescription>
                <CardAction>
                    <ClaimButton pr_id={props.pr_id} payout={props.payout} />
                </CardAction>
            </CardHeader>
        </Card>
    )
}