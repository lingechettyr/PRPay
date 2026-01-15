'use client';

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { useSidebar } from "@/components/ui/sidebar";

export default function UserDisplay() {
    const {state} = useSidebar()
    return (
          <div 
            className="w-full flex justify-start gap-3"
          >
            <Avatar className={state === "expanded" ? `w-10 h-10` : `w-5 h-5`}>
              <AvatarImage src="https://api.dicebear.com/7.x/avataaars/svg?seed=shadcn" />
              <AvatarFallback>
                SC
              </AvatarFallback>
            </Avatar>
            { state === "expanded" && (
                <div className="flex-1 text-left min-w-0">
                    <div className="font-medium text-sm truncate">shadcn</div>
                    <div className="text-xs text-zinc-400 truncate">m@example.com</div>
                </div>
            )}
          </div>
    )
}