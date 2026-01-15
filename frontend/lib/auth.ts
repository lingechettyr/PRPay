import { supabase } from '@/lib/supabase/client'

export async function signInWithGithub() {
  const { error } = await supabase.auth.signInWithOAuth({
    provider: 'github',
    options: {
      redirectTo: `${process.env.NEXT_PUBLIC_BASE_URL}/auth/callback`
    },
  });
  if (error) {
    console.error('Error during GitHub sign-in:', error.message);
  }
}