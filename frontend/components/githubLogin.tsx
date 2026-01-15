'use client'

import { Button } from "@/components/ui/button";
import { Github } from "lucide-react";
import { signInWithGithub } from "@/lib/auth";

export default function GithubLogin() {
    return (
        <Button className="w-full flex items-center gap-2 hover:cursor-pointer" variant="outline" onClick={signInWithGithub}>
        <Github className="h-5 w-5"/>
          Login with GitHub
        </Button>
    )
}