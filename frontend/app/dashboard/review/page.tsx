
import ReviewPR from "@/components/events/reviewPr";
import ReviewPRProps from "@/components/events/types";
import { createClient } from "@/lib/supabase/server";

export default async function ReviewPage(){
    const supabase = await createClient();
    const { data: { user } } = await supabase.auth.getUser()

    // GitHub ID is here:
    const githubId = user?.user_metadata?.provider_id

    const params = new URLSearchParams({
        user_id: githubId,
        status: "requested"
    });
    const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}getPRs?${params}`, {
        cache: "no-store"
    });
    const data: ReviewPRProps[]  = await res.json();
    console.log("Review PRs Data:", data);

    return (
        <div className="flex flex-col">
            {data.map((pr) => (
                <ReviewPR 
                    key={pr.pr_id}
                    pr_id={pr.pr_id}
                    pr_title={pr.pr_title}
                    pr_created_at={pr.pr_created_at}
                    pr_url={pr.pr_url}
                    payout={pr.payout}
                />
            ))}
        </div>
    )
}