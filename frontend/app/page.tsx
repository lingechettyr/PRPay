import { Card, CardHeader, CardTitle, CardContent} from "@/components/ui/card";
import GithubLogin from "@/components/githubLogin";

export default function Home() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-background">
    <Card className="w-full max-w-sm shadow-lg rounded-2xl">
      <CardHeader className="text-center">
        <CardTitle className="text-2xl">PRPay</CardTitle>
        {/* TODO: Add an image instead of a text. */}
      </CardHeader>
      <CardContent className="flex flex-col gap-4">
        <GithubLogin />
      </CardContent>
    </Card>
  </div>
  );
}
