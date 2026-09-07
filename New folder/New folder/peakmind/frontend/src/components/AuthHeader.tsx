'use client';

import { SignInButton, UserButton, useAuth } from '@clerk/nextjs';

export function AuthHeader() {
  const { isSignedIn } = useAuth();

  return (
    <div>
      {!isSignedIn ? (
        <SignInButton mode="modal">
          <button className="px-4 py-2 bg-brand-600 hover:bg-brand-500 rounded-md font-medium text-white transition-colors">
            Sign In
          </button>
        </SignInButton>
      ) : (
        <UserButton />
      )}
    </div>
  );
}
