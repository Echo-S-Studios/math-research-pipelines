default(parisize, "2048M");

tracedown(f) = {
  \\ f self-reciprocal in x, even degree 2m: returns D with f = lc * x^m * D(x+1/x)
  my(m = poldegree(f)/2, T = vector(m+1), D);
  T[1] = 2; if(m >= 1, T[2] = 't);
  for(k = 2, m, T[k+1] = 't*T[k] - T[k-1]);
  D = polcoef(f, m, x);
  for(k = 1, m, D += polcoef(f, m+k, x) * T[k+1]);
  D;
}

scan(cv, n) = {
  my(P = y^n + sum(k = 0, n-1, cv[k+1]*y^k));
  my(R = polresultant(P, subst(P, y, x*y), y));
  my(D5 = divrem(R, (x-1)^n));
  if(D5[2] != 0, print("GPN4 STRIP-FAIL ", cv); return);
  my(Rat0 = D5[1]); Rat0 = Rat0/content(Rat0)*sign(pollead(Rat0));
  \\ full-Rat cyclotomic signature (expect Phi1^n only)
  my(fr = factor(R), sigr = List());
  for(i = 1, matsize(fr)[1],
    my(k = poliscyclo(fr[i,1])); if(k, listput(sigr, [k, fr[i,2]])));
  \\ S* selection: self-reciprocal even factors with unimodular roots
  my(fa = factor(Rat0), Sstar = 1, det = 0);
  for(i = 1, matsize(fa)[1],
    my(f = fa[i,1], df = poldegree(f), fm);
    fm = f/pollead(f);
    if(df % 2 == 0 && fm == polrecip(fm)/polcoef(polrecip(fm), df),
      my(td = tracedown(fm), cnt = polsturm(td, [-2, 2]));
      if(cnt > 0, Sstar *= fm; det += cnt)));
  my(d = poldegree(Sstar));
  my(G = sum(k = 0, d, polcoef(Sstar, k, x)*x^k*y^(d-k)));
  my(C2 = polresultant(subst(Sstar, x, y), G, y));
  my(fc = factor(C2), sig = List(), noncyc = 0);
  for(i = 1, matsize(fc)[1],
    my(k = poliscyclo(fc[i,1]));
    if(k, listput(sig, [k, fc[i,2]]), noncyc += poldegree(fc[i,1])*fc[i,2]));
  print("GPN4 n=", n, " c=", cv, " ratsig=", Vec(sigr),
        " degS*=", d, " det=", det, " c2sig=", Vec(sig),
        " c2noncyc=", noncyc, " degC2=", poldegree(C2));
}

scan([-2,-2,-2,-2,-2], 5);
scan([-2,-2,-2,-2,-2,-2], 6);
scan([1,-1,-2,2,2,-2,-2], 7);
scan([-2,-2,-2,-2,-2,-2,-2], 7);
quit
