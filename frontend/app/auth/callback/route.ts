import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'
// The client you created from the Server-Side Auth instructions

export async function GET(request: Request) {
  const { searchParams, origin } = new URL(request.url)
  const code = searchParams.get('code')
  // if "next" is in param, use it as the redirect URL
  let next = searchParams.get('next') ?? '/dashboard'
  
  console.log('=== AUTH CALLBACK DEBUG ===')
  console.log('Code exists:', !!code)
  console.log('Next param from URL:', searchParams.get('next'))
  console.log('Next value before check:', next)
  
  if (!next.startsWith('/')) {
    // if "next" is not a relative URL, use the default
    console.log('Next does not start with /, changing to /')
    next = '/'
  }
  
  console.log('Final next value:', next)

  if (code) {
    const supabase = await createClient()
    const { error } = await supabase.auth.exchangeCodeForSession(code)
    
    console.log('Exchange error:', error)
    
    if (!error) {
      const forwardedHost = request.headers.get('x-forwarded-host') // original origin before load balancer
      const isLocalEnv = process.env.NODE_ENV === 'development'
      
      const redirectUrl = isLocalEnv 
        ? `${origin}${next}` 
        : forwardedHost 
          ? `https://${forwardedHost}${next}` 
          : `${origin}${next}`
      
      console.log('Redirecting to:', redirectUrl)
      
      if (isLocalEnv) {
        // we can be sure that there is no load balancer in between, so no need to watch for X-Forwarded-Host
        return NextResponse.redirect(`${origin}${next}`)
      } else if (forwardedHost) {
        return NextResponse.redirect(`https://${forwardedHost}${next}`)
      } else {
        return NextResponse.redirect(`${origin}${next}`)
      }
    }
  }

  // return the user to an error page with instructions
  console.log('No code or error occurred, redirecting to error page')
  return NextResponse.redirect(`${origin}/auth/auth-code-error`)
}