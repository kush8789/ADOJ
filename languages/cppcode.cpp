#include<bits/stdc++.h>
using namespace std;
int main()
{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    cout.tie(NULL);
    long long int n;
    long long int sum=0;
    cin>>n;
    long long a[n],prefix_sum[n];
    for(long long i=1;i<=n;i++)
    {
        cin>>a[i];
        sum+=a[i];
        prefix_sum[i]=sum;
    }
    long long q;
    cin>>q;
    while(q--)
    {
        long long l,r;
        cin>>l>>r;
        if(l==1)
        {
            cout<<prefix_sum[r]<<endl;
        }
        else
        {
            cout<<prefix_sum[r]-prefix_sum[l-1]<<endl;
        }
    }
    return 0;
}