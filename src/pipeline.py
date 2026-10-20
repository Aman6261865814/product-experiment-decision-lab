
from common import *

def evaluate(df):
    counts=df.groupby('variant').size().reindex(['control','treatment'],fill_value=0)
    srm=float(stats.chisquare(counts).pvalue)
    a=df[df.variant=='control'];b=df[df.variant=='treatment']
    if min(len(a),len(b))==0:raise ValueError('Both randomized arms required')
    p0=a.converted.mean();p1=b.converted.mean();delta=p1-p0
    se=np.sqrt(p0*(1-p0)/len(a)+p1*(1-p1)/len(b))
    pooled=(a.converted.sum()+b.converted.sum())/len(df)
    nullse=np.sqrt(pooled*(1-pooled)*(1/len(a)+1/len(b)))
    pvalue=float(2*stats.norm.sf(abs(delta/nullse))) if nullse else 1.
    ci=[float(delta-1.96*se),float(delta+1.96*se)]
    crash_delta=b.crashed.mean()-a.crashed.mean()
    crashse=np.sqrt(a.crashed.mean()*(1-a.crashed.mean())/len(a)+b.crashed.mean()*(1-b.crashed.mean())/len(b))
    # One-sided 95% upper bound for a prespecified noninferiority guardrail.
    crash_upper=float(crash_delta+stats.norm.ppf(.95)*crashse)
    decision='INVALID: investigate assignment' if srm<.001 else ('SHIP' if ci[0]>.005 and crash_upper<.005 else 'HOLD')
    return {'users':len(df),'control_users':len(a),'treatment_users':len(b),'srm_p_value':srm,'control_conversion':float(p0),
      'treatment_conversion':float(p1),'conversion_delta_pp':float(delta*100),'conversion_ci95_pp':[x*100 for x in ci],
      'conversion_p_value':pvalue,'crash_delta_pp':float(crash_delta*100),'crash_upper95_pp':crash_upper*100,'decision':decision}

def run():
    rng=np.random.default_rng(SEED);n=30000
    variant=rng.choice(['control','treatment'],n)
    converted=rng.binomial(1,np.where(variant=='treatment',.139,.12))
    raw=pd.DataFrame({'user_id':np.arange(n)+1,'variant':variant,'region':rng.choice(['Americas','EMEA','APAC'],n),
       'device':rng.choice(['desktop','mobile'],n,p=[.55,.45]),'assigned_date':pd.Timestamp('2026-05-01')+pd.to_timedelta(rng.integers(0,14,n),unit='D'),
       'converted':converted,'crashed':rng.binomial(1,np.where(variant=='treatment',.022,.020)),
       'revenue_usd':np.round(converted*rng.lognormal(3.5,.8,n),2)})
    raw.assigned_date=raw.assigned_date.dt.strftime('%Y-%m-%d')
    raw=pd.concat([raw,raw.sample(150,random_state=SEED)],ignore_index=True)
    write(raw,'assignment_outcomes','raw');df,removed=load_clean(raw,['user_id'])
    metrics=evaluate(df);metrics['duplicate_retries_removed']=removed
    a=df[df.variant=='control'].revenue_usd.to_numpy();b=df[df.variant=='treatment'].revenue_usd.to_numpy()
    metrics['exploratory_revenue_delta_usd']=float(b.mean()-a.mean())
    metrics['exploratory_revenue_ci95_usd']=bootstrap_mean_diff(a,b)
    # Normal approximation, equal allocation, 80% power, two-sided alpha=.05.
    metrics['planned_users_per_arm']=int(np.ceil(2*(stats.norm.ppf(.975)+stats.norm.ppf(.8))**2*.12*.88/.015**2))
    grouped=df.groupby('variant',as_index=False).agg(users=('user_id','count'),conversions=('converted','sum'),crashes=('crashed','sum'),revenue_usd=('revenue_usd','sum'))
    grouped['conversion_rate']=grouped.conversions/grouped.users
    grouped['crash_rate']=grouped.crashes/grouped.users
    segments=df.groupby(['variant','device'],as_index=False).agg(users=('user_id','count'),conversions=('converted','sum'))
    summary=f"""## Decision: {metrics['decision']}\nConversion change is {metrics['conversion_delta_pp']:.2f} percentage points (95% CI {metrics['conversion_ci95_pp'][0]:.2f} to {metrics['conversion_ci95_pp'][1]:.2f}). Assignment SRM p={metrics['srm_p_value']:.4f}. Crash-rate one-sided upper bound is {metrics['crash_upper95_pp']:.2f} pp; guardrail limit is +0.50 pp.\n\n## Prespecified policy\nAnalyze once after all users have 7 days of follow-up; assignment May 1–14, extraction May 22, 2026. Intent-to-treat unit is user. SRM threshold .001. Ship only if conversion CI lower bound exceeds +0.50 pp AND crash upper bound is below +0.50 pp. Planned MDE +1.50 pp at 80% power requires approximately {metrics['planned_users_per_arm']:,} users/arm. No optional stopping.\n\n## Limits\nRevenue bootstrap and device slices are exploratory, not additional launch criteria; no segment winner claims. Synthetic independent users cannot establish real customer lift. Missing outcomes are absent by construction; production must monitor missingness and exposure logging. Normal approximations require sufficient successes/failures; use exact methods for sparse experiments.\n"""
    def charts():
        fig,ax=plt.subplots(figsize=(8,4));sns.barplot(data=grouped,x='variant',y='conversion_rate',ax=ax,color='#2563eb');ax.set(title='Seven-day conversion | synthetic randomized users',ylabel='Conversion proportion',ylim=(0,.18));fig.tight_layout();fig.savefig(ROOT/'reports'/'conversion.png',dpi=160);plt.close(fig)
        fig,ax=plt.subplots(figsize=(8,3));d=metrics['conversion_delta_pp'];lo,hi=metrics['conversion_ci95_pp'];ax.errorbar(d,0,xerr=[[d-lo],[hi-d]],fmt='o',capsize=6);ax.axvline(0,color='gray');ax.axvline(.5,color='#e87924',linestyle='--',label='Minimum meaningful lift');ax.set(title='Treatment effect and 95% confidence interval',xlabel='Conversion change (percentage points)',yticks=[]);ax.legend();fig.tight_layout();fig.savefig(ROOT/'reports'/'effect_interval.png',dpi=160);plt.close(fig)
    finish({'fact_experiment':df,'variant_metrics':grouped,'device_segments':segments},metrics,summary,'Product Experiment Decision Lab',charts)

if __name__=='__main__':run()
