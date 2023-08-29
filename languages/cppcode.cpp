#include<bits/stdc++.h>
#define mod 1000000007
using namespace std;
int get(int n,vector<int> &dp)
{
    if(n<=2)
    return n;
    
    if(dp[n]!=-1)
    return dp[n];
    
  dp[n]=(get(n-1,dp)+get(n-2,dp))%mod;
  return dp[n];
}
int main()
{
    int n;
    cin>>n;
    vector<int>dp(n+1,-1);
    cout<<get(n,dp);
    return 0;
}