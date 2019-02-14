
4.

remove all x from string, then remove all be from string, then remove all bye from string, you should get empty string.

5.

a. Only infinite regular language can be pumped into this fashion. The regular expr `abc` is a regular language, 
    and it doesn't violate the theorm (just let M=4). Such language has a maximum string length N, we let M=N+1 so 
    this theorm is not violated.

   Characterize the set of all such machines:
    There's no loop in the FSA.

b. let M = (state_of(F) + 1). It always works.

c. Since the FSA has N states, every character in the string is on one state. Since stringLength = L >= M > N, 
    the character - string mapping should look like: (Pigeon Hole Principle)

    c0 c1 c2 c3 ... ck ck+1 ... cm cm+1 ... cL-2 cL-1

    s0 s1 s2 ... .. sk sk+1 ... sk sk+1 ... sN-2 sN-1

    So there must be some substring [ck ck+1 ... cm] is read by state [sk ... sk].

    let u = [c0 ... ck-1]
    let x = [ck ... cm-1]
    let v = [cm ... cL-1]

    return u, x, v

d.  Assume, for the sake of contradiction, that the FSA exists.
    Let M be the minimum length as in the pumping lemma, for the existing FSA.
    I can pick an example string `S = yy^r`, whose `len(S) == 2*M` and `len(y) == M`. The string S is
    accepted by the FSA.

    Then there is a decomposition `S = uxv` such that `|x| > 0`, `|ux| ≤ M`, and `u x^n v ∈ A`
    for all n ≥ 0. So `uv ∈ A` is always true (n=0).

    Since |ux| ≤ M, the substring ux must be entirely contained within the first half substring "y" of S.

    S:
    |----------y----------|----------y^r-----------|
    |-----u-----|--x--|------------v---------------|

    |-----u-----|     |------------v---------------|
                       ^              ^

    `uv ∈ A` is always true => `S[len(u)+1] == S[len(S) - len(u)-1]`
    Obviously, it's not always true.

    This is a contradiction, and consequently the FSA doesn't exist.

6.    



    

