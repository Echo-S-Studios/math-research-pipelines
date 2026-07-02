contacts(R) = {
  my(F = factor(R), v = List());
  for(i = 1, matsize(F)[1],
    if(type(F[i,1]) == "t_POL" && poldegree(F[i,1]) > 0,
      my(n = poliscyclo(F[i,1]));
      if(n, listput(v, [n, F[i,2]]))));
  vecsort(Vec(v))
}
rat(p) = polresultant(subst(p, x, 'y), subst(p, x, x*'y), 'y);
p  = x^4 - x + 1;
S6 = x^6 - x^4 - x^3 - x^2 + 1;
print("X1 ", contacts(rat(p)));
prodpoly = polresultant(subst(p, x, 'y), 'y^4 * subst(p, x, x/'y), 'y);
F = factor(prodpoly / pollead(prodpoly));
print("X2 ", vecsort(vector(matsize(F)[1], i, [Str(F[i,1]), F[i,2]])));
print("X3 S6^2 divides: ", prodpoly % S6^2 == 0);
quit
