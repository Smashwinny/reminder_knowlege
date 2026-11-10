"""原创教学程序：仅 numpy；不是 LingBot-Map 推理或完整 SLAM/VIO。"""
import argparse,json,sys,platform
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent

def env():
    return {'python':sys.version.split()[0],'numpy':np.__version__,'platform':platform.platform(),'cuda_devices':len(list(Path('/dev').glob('nvidia[0-9]*'))),'scope':'CPU synthetic numerical experiments; no model weights'}

def scale():
    rng=np.random.default_rng(42); X=rng.uniform([-2,-1,4],[2,1,10],(200,3)); C=np.array([.7,.2,0.])
    def project(x,c):
        a=x-c;return 500*a[:,:2]/a[:,2:]+np.array([259,189])
    e=float(np.max(abs(project(X,C)-project(3.7*X,3.7*C))))
    assert e<1e-10
    return {'points':len(X),'scale':3.7,'max_pixel_difference':e,'claim':'same projections do not identify metric scale'}

def context():
    # Actual resolution 518/14 by 378/14 = 37*27 image tokens.
    M=37*27; n=8;k=64;rows=[]
    for T in [320,1000,10000,100000]:
        causal=T*(M+6);gca=(n+k)*M+6*T
        rows.append({'frames':T,'causal_tokens':causal,'gca_tokens':gca,'ratio':causal/gca})
    slope=((n+k)*M+6*10001)-((n+k)*M+6*10000)
    assert slope==6 and rows[-1]['gca_tokens']>rows[-2]['gca_tokens']
    return {'M':M,'anchors':n,'window':k,'rows':rows,'increment_per_frame':slope,'scope':'analytical token counts, not GPU memory measurement'}

def graph():
    # 2D translation-only pose graph with a hard fixed first pose.
    t=np.linspace(0,2*np.pi,61); gt=np.c_[5*(np.cos(t)-1),5*np.sin(t)]
    rng=np.random.default_rng(7); z=np.diff(gt,axis=0)+np.array([.025,-.015])+rng.normal(0,.01,(60,2))
    od=np.vstack([np.zeros(2),np.cumsum(z,axis=0)])
    def solve(loop):
        A=[];b=[]
        for i in range(60):
            row=np.zeros(60)
            if i>0:row[i-1]=-1
            row[i]=1;A.append(row/.03);b.append(z[i]/.03)
        row=np.zeros(60);row[-1]=1;A.append(row/.01);b.append(np.array(loop)/.01)
        A=np.array(A);b=np.array(b);x=np.linalg.lstsq(A,b,rcond=None)[0]
        return np.vstack([np.zeros(2),x]),float(np.linalg.norm(A.T@(A@x-b)))
    good,normal=solve([0,0]);bad,_=solve([4,0])
    def metrics(x):return {'rmse_m':float(np.sqrt(np.mean(np.sum((x-gt)**2,axis=1)))),'endpoint_error_m':float(np.linalg.norm(x[-1]-gt[-1]))}
    a,b,c=metrics(od),metrics(good),metrics(bad)
    assert b['rmse_m']<a['rmse_m'] and c['rmse_m']>a['rmse_m'] and normal<1e-7
    np.savez(ROOT/'graph-data.npz',truth=gt,odometry=od,good_loop=good,bad_loop=bad)
    return {'poses':61,'odometry':a,'correct_loop':b,'wrong_loop':c,'normal_equation_residual':normal,'scope':'linear weighted least squares = one exact Gauss-Newton step; no rotation/visual front-end'}

def imu():
    # 1D gravity-removed constant acceleration; fixed orientation.
    dt=.005;N=400;true_a=.4;bias=.05;measured=true_a+bias
    def integrate(a):
        p=v=0.
        for i in range(N):p+=v*dt+.5*a*dt*dt;v+=a*dt
        return p,v
    p,v=integrate(measured);T=dt*N;pc=p-.5*bias*T*T;vc=v-bias*T
    truth_p=.5*true_a*T*T;truth_v=true_a*T
    assert abs(pc-truth_p)<1e-12 and abs(vc-truth_v)<1e-12
    return {'samples':N,'dt_s':dt,'duration_s':T,'raw_delta_p_m':p,'raw_delta_v_m_s':v,'true_delta_p_m':truth_p,'true_delta_v_m_s':truth_v,'bias_corrected_delta_p_m':pc,'bias_corrected_delta_v_m_s':vc,'bias_position_error_m':p-truth_p,'scope':'1D preintegration intuition only; no SO(3), covariance, noise or full VIO'}

def verify():
    funcs=[env,scale,context,graph,imu]; out={f.__name__:f() for f in funcs}
    (ROOT/'results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
    return {'groups_passed':len(funcs),'scope':'author-written deterministic checks, not independent audit or upstream tests'}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('step',choices=['env','scale','context','graph','imu','verify']);a=ap.parse_args()
    print(json.dumps(globals()[a.step](),ensure_ascii=False,indent=2))
