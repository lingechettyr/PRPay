import { GitBranch } from "lucide-react";
import { Button } from "../ui/button";
import { Card, CardAction, CardDescription, CardHeader, CardTitle } from "../ui/card";
import ReviewPRProps from "./types";

export default function ReviewPR(props: ReviewPRProps){
    return (
        <Card className="w-full bg-sky-300/20">
            <CardHeader>
                <CardTitle>{props.pr_title}</CardTitle>
                <CardDescription>{props.pr_created_at}</CardDescription>
                <CardAction>
                    <Button variant="outline" className="hover:cursor-pointer" asChild >
                        <a href={props.pr_url} target="_blank" rel="noopener noreferrer">
                        <GitBranch />
                        View on GitHub
                        </a>
                    </Button>
                </CardAction>
            </CardHeader>
        </Card>
    )
}