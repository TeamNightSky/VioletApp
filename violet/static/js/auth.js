import 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js'

const client = supabase.createClient('https://uidobsmxjjjrjspmrvev.supabase.co', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJvbGUiOiJhbm9uIiwiaWF0IjoxNjQyOTY0MDk3LCJleHAiOjE5NTg1NDAwOTd9.1NFrxinSciPQ-ngkI-3QwvdEVJtCu9ysq34Nww7_pzM')


function register(provider) {
    const { user, session, error } = client.auth.signIn({
      // provider can be only discord rn
      provider: provider
    }, {
      redirectTo: 'https://VioletApp.grandmoff100.repl.co/register_success.html'
    });
}
window["register"] = register;
