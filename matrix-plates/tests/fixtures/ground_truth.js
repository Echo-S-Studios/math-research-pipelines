"use strict";
/* ==== verbatim functions lifted from matrix_plates.html ==== */
const zeros=n=>Array.from({length:n},()=>new Array(n).fill(0));
const clone=A=>A.map(r=>r.slice());
const trace=A=>{let t=0;for(let i=0;i<A.length;i++)t+=A[i][i];return t;};
function matmul(A,B){const n=A.length,p=B[0].length,m=B.length,C=Array.from({length:n},()=>new Array(p).fill(0));
  for(let i=0;i<n;i++)for(let k=0;k<m;k++){const a=A[i][k];if(!a)continue;for(let j=0;j<p;j++)C[i][j]+=a*B[k][j];}return C;}
function addScaledI(A,c){const B=clone(A);for(let i=0;i<B.length;i++)B[i][i]+=c;return B;}
function charPoly(A){
  const n=A.length;if(n===0)return{coeffs:[1],det:1};
  const c=[];let M=clone(A);
  for(let k=1;k<=n;k++){
    if(k>1){const T=addScaledI(M,c[k-2]);M=matmul(A,T);}
    c.push(-trace(M)/k);
  }
  const coeffs=[1,...c.map(v=>Math.round(v))];
  const det=Math.round(Math.pow(-1,n)*coeffs[n]);
  return{coeffs,det};
}
function mulberry32(seed){let a=seed>>>0;return()=>{a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};}
function randIntMat(n,seed){const rnd=mulberry32(seed),C=zeros(n);
  for(let i=0;i<n;i++)for(let j=0;j<n;j++)C[i][j]=Math.floor(rnd()*7)-3;return C;}
function companion(poly){
  const n=poly.length-1,C=zeros(n);
  for(let i=1;i<n;i++)C[i][i-1]=1;
  for(let i=0;i<n;i++)C[i][n-1]=-poly[n-i];
  return C;}
function kron(A,B){const n=A.length,m=B.length,C=zeros(n*m);
  for(let i=0;i<n;i++)for(let j=0;j<n;j++)for(let k=0;k<m;k++)for(let l=0;l<m;l++)C[i*m+k][j*m+l]=A[i][j]*B[k][l];return C;}
function dsum(A,B){const n=A.length,m=B.length,C=zeros(n+m);
  for(let i=0;i<n;i++)for(let j=0;j<n;j++)C[i][j]=A[i][j];
  for(let i=0;i<m;i++)for(let j=0;j<m;j++)C[n+i][n+j]=B[i][j];return C;}
function commutator(A,B){const AB=matmul(A,B),BA=matmul(B,A),n=A.length,C=zeros(n);
  for(let i=0;i<n;i++)for(let j=0;j<n;j++)C[i][j]=AB[i][j]-BA[i][j];return C;}
function frustratedRing(n){
  const W=zeros(n);
  for(let i=0;i<n;i++){const j=(i+1)%n,s=(i%2===0)?-1:1;W[i][j]+=s;W[j][i]+=s;}
  const L=zeros(n);
  for(let i=0;i<n;i++){let d=0;for(let j=0;j<n;j++)d+=Math.abs(W[i][j]);L[i][i]=d;for(let j=0;j<n;j++)if(j!==i)L[i][j]=-W[i][j];}
  return L;}
function fibWord(n){const a=[1,1];while(a.length<n)a.push(a[a.length-1]+a[a.length-2]);return a.slice(0,n);}
function lucasWord(n){const a=[2,1];while(a.length<n)a.push(a[a.length-1]+a[a.length-2]);return a.slice(0,n);}
function circulant(row){const n=row.length,C=zeros(n);for(let i=0;i<n;i++)for(let j=0;j<n;j++)C[i][j]=row[(j-i+n)%n];return C;}
function cartanEdges(n,edges){const A=zeros(n);for(let i=0;i<n;i++)A[i][i]=2;for(const[a,b]of edges){A[a][b]=-1;A[b][a]=-1;}return A;}
function cartanA(n){const e=[];for(let i=0;i<n-1;i++)e.push([i,i+1]);return cartanEdges(n,e);}
function cartanD(n){const e=[];for(let i=0;i<=n-3;i++)e.push([i,i+1]);e.push([n-3,n-1]);return cartanEdges(n,e);}
function cartanE8(){return cartanEdges(8,[[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[2,7]]);}

/* ==== emit ground truth ==== */
const out = {};
out.mulberry32_42_first8 = (()=>{const r=mulberry32(42);return Array.from({length:8},()=>r());})();
out.mulberry32_7_first8  = (()=>{const r=mulberry32(7); return Array.from({length:8},()=>r());})();
out.randIntMat_4_42 = randIntMat(4,42);
out.randIntMat_4_7  = randIntMat(4,7);
out.randIntMat_3_123 = randIntMat(3,123);
out.companion_phi = companion([1,-1,-1]);
out.companion_sq2 = companion([1,0,-2]);
out.companion_gap = companion([1,-7,1]);
out.companion_K   = companion([1,0,5,0,-5]);
out.companion_cons= companion([1,-6,26,-16,-4]);
out.companion_res = companion([1,2,39,-52,11]);
out.phi_dsum_phi  = dsum(companion([1,-1,-1]),companion([1,-1,-1]));
out.companion_of_phi2 = companion([1,-2,-1,2,1]);   // (x^2-x-1)^2
out.kron_phi_sq3  = kron(companion([1,-1,-1]),companion([1,0,-3]));
out.cartanE8 = cartanE8();
out.cartanA5 = cartanA(5);
out.cartanD4 = cartanD(4);
out.fibcirc6 = circulant(fibWord(6));
out.ring6 = frustratedRing(6);
out.ring5 = frustratedRing(5);
out.charpoly_E8 = charPoly(cartanE8());
out.charpoly_phidsumphi = charPoly(dsum(companion([1,-1,-1]),companion([1,-1,-1])));
out.charpoly_fibcirc6 = charPoly(circulant(fibWord(6)));
out.charpoly_ring6 = charPoly(frustratedRing(6));
out.charpoly_ring5 = charPoly(frustratedRing(5));
console.log(JSON.stringify(out,null,1));
