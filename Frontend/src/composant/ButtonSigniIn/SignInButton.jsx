import { useMsal } from '@azure/msal-react';

export const SignInButton = () => {
    const{instance} = useMsal();

    const handleSigneIn = () => (
        instance.loginRedirect({
            scopes: ['user.read']
        })
    )

    return (
        <button onClick={handleSigneIn}>Sign In</button>
    )
};