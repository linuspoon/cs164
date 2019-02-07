# cs164 lab

## Submit guide

http://inst.eecs.berkeley.edu/~cs164/sp19/git.html

## ssh config

```
### berkeley

Host cs164_router
    Hostname ashby.cs.berkeley.edu
    User cs164-ace

Host cs164
    #ProxyJump cs164_router
    Hostname ashby.cs.berkeley.edu
    User cs164-taa
    IdentityFile ~/keys/cs164.privkey
```

