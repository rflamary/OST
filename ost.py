# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 09:40:14 2016

@author: Rémi Flamary
"""
import numpy as np
import scipy.fftpack

def get_metric(metric,midi_notes,Fe,nfft,nz=1e4,eps=10,**kwargs):
    """
    returns the optimal transport loss matrix from a list of midi notes (interger indexes)
    """
    nbnotes=len(midi_notes)
    res=np.zeros((nfft//2,nbnotes))
    f=np.fft.fftfreq(nfft,1.0/Fe)[:nfft//2]
    f_note=[2.0**((n-60)*1./12)*440 for n in midi_notes]
    for i in range(nbnotes):
        m=np.zeros((nfft//2,))
        if metric=='square':
            m=(f_note[i]-f)**2
        elif metric=='psquare':
            if midi_notes[i]==0:
                m[:]=nz
            else:
                nmax=int(f.max()/f_note[i])
                m[:]=np.inf
                for j in range(1,nmax+1):
                    m=np.minimum(m,(j*f_note[i]-f)**2+j*eps)
        res[:,i]=m



    return res,f

def unmix_plan_fundamental(midi_notes,Fe,nfft):
    """
    returns the index of the sample nearest from the fundamental for each midi
    
    Those indexes can be used for simple poxer based unmixing

    """
    f=np.fft.fftfreq(nfft,1.0/Fe)[:nfft//2]
    f_note=[2.0**((n-60)*1./12)*440 for n in midi_notes]
    return [np.argmin((fn-f)**2) for fn in f_note]

def unmix_fun_fundamental(idfund):
    """
    returns the unmixing function for fundamental power using the index of fundamentals
    """
    nb=len(idfund)
    def f(x,idf=idfund):
        res=np.zeros((nb,))
        for i in range(len(idf)):
            res[i]=x[idf[i]]
        res/=res.sum()
        return res
    return f

def unmix_plan_lp(M):
    """
    returns the index of the note with minimum cost for each sample (OST unmixing)
    """
    return [np.argmin(M[i,:]) for i in range(M.shape[0])]

def unmix_fun_lp(idlp,nb):
    """
    returns the unmixing function for OST unmixing (using idlp pre-computed plan)
    """
    def f(x,idf=idlp,nb=nb):
        res=np.zeros((nb,))
        for i in range(len(idf)):
            res[idf[i]]+=x[i]
        return res
    return f

def unmix_fun_lp_sparse(M,mu,nbiter=2,eps=1e-6,**kwargs):
    nb=M.shape[1]
    """
    returns the unmixing function for sparse OST unmixing 
    """
    def f(x,M=M,mu=mu,nbiter=nbiter,eps=eps):
        w=np.zeros((1,nb))
        for it in range(nbiter):
            res=np.zeros((nb,))
            Mcur=M+w
            for i in range(M.shape[0]):
                isel=np.argmin(Mcur[i,:])
                res[isel]+=x[i]
            w=mu*1.0/(np.sqrt(res)+eps)
        return res

    return f


def unmix_plan_entrop(M,lambd):
    """
    returns the rpe compute L plan for entropic regularized OST

    """
    E=np.exp(-M/lambd/M.max())
    return E*1./(E.sum(1).reshape((M.shape[0],1)))

def unmix_fun_entrop(L):
    """
    returns the unmixing function for entropic OST unmixing 
    """    
    def f(x,L=L):
        return L.T.dot(x)
    return f

def get_unmix_fun(midi_notes,Fe,nfft,method='fund',metric='psquare',lambd=1e-3,**kwargs):
    """
    returns the unmixing function for all methods (easy to change)

    """
    if method.lower()=='fund':
        idfund=unmix_plan_fundamental(midi_notes,Fe,nfft)
        f=unmix_fun_fundamental(idfund)
    elif method.lower() in ['lp','ost']:
        M,f=get_metric(metric,midi_notes,Fe,nfft,**kwargs)
        idlp=unmix_plan_lp(M)
        f=unmix_fun_lp(idlp,nfft//2)
    elif method.lower() in ['oste','entrop']:
        M,f=get_metric(metric,midi_notes,Fe,nfft,**kwargs)
        L=unmix_plan_entrop(M,lambd)
        f=unmix_fun_entrop(L)
    elif method.lower() in ['lp_sparse','ost_sparse','ostg']:
        M,f=get_metric(metric,midi_notes,Fe,nfft,**kwargs)
        f=unmix_fun_lp_sparse(M,**kwargs)
    return f
