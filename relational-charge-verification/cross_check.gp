contacts(R) = {
  my(F = factor(R), v = List());
  for(i = 1, matsize(F)[1],
    if(type(F[i,1]) == "t_POL" && poldegree(F[i,1]) > 0,
      my(n = poliscyclo(F[i,1]));
      if(n, listput(v, [n, F[i,2]]))));
  vecsort(Vec(v))
}
rat(p)      = polresultant(subst(p, x, 'y), subst(p, x, x*'y), 'y);
mixed(p, q) = polresultant(subst(q, x, 'y), subst(p, x, x*'y), 'y);
b4 = x^4-x^3-x^2-x+1;
L  = x^10+x^9-x^7-x^6-x^5-x^4-x^3+x+1;
print("A ", contacts(rat(x^3-2)));
print("B ", contacts(rat(x^3+2)));
print("C ", contacts(rat(x^4-2)));
print("D ", contacts(rat(x^4+x^2-1)));
print("E ", contacts(rat(x^4+5*x^2+5)));
print("F ", contacts(rat(x^4+5*x^2-5)));
print("G ", contacts(rat(b4)));
print("H ", contacts(rat(L)));
print("I ", contacts(mixed(L, b4)));
print("gpversion ", version());
S6 = x^6-x^4-x^3-x^2+1;
S8 = x^8-x^5-x^4-x^3+1;
print("P1 ", contacts(rat(S6)));
print("P2 ", contacts(rat(S8)));
print("Q1 ", contacts(mixed(S6, b4)));
print("Q2 ", contacts(mixed(S8, b4)));
print("Q3 ", contacts(mixed(S8, S6)));
print("Q4 ", contacts(mixed(L, S6)));
print("Q5 ", contacts(mixed(L, S8)));
