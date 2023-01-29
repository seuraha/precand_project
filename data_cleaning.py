import re
import pandas as pd
import numpy as np

def time_colval(*columns):
    for x in columns:
        if len(x) != len(columns)-1:
            continue
        
        d = x.to_dict()
        
        for k, v in d.items():
            val = int(re.findall("\d+", str(k))[0])
            if v == 3:
                return val

        if d["time_pref246"] == 1:
            if d["time_pref296"] == 1:
                if d["time_pref323"] == 1:
                    if d["time_pref336"] == 1:
                        if d["time_pref343"] == 1:
                            return 344
                        else:
                            return 342
                    else:
                        if d["time_pref329"] == 1:
                            return 330
                        else:
                            return 328
                else:
                    if d["time_pref309"] == 1:
                        if d["time_pref316"] == 1:
                            return 317
                        else:
                            return 315
                    else:
                        if d["time_pref303"] == 1:
                            return 304
                        else:
                            return 302
            else:
                if d["time_pref270"] == 1:
                    if d["time_pref283"] == 1:
                        if d["time_pref290"] == 1:
                            return 291
                        else:
                            return 289
                    else:
                        if d["time_pref277"] == 1:
                            return 278
                        else:
                            return 276
                else:
                    if d["time_pref258"] == 1:
                        if d["time_pref264"] == 1:
                            return 265
                        else:
                            return 263
                    else:
                        if d["time_pref252"] == 1:
                            return 253
                        else:
                            return 251
        else:
            if d["time_pref201"] == 1:
                if d["time_pref223"] == 1:
                    if d["time_pref234"] == 1:
                        if d["time_pref240"] == 1:
                            return 241
                        else:
                            return 239
                    else:
                        if d["time_pref228"] == 1:
                            return 229
                        else:
                            return 227
                else:
                    if d["time_pref212"] == 1:
                        if d["time_pref217"] == 1:
                            return 218
                        else:
                            return 216
                    else:
                        if d["time_pref206"] == 1:
                            return 207
                        else:
                            return 205
            else:
                if d["time_pref180"] == 1:
                    if d["time_pref190"] == 1:
                        if d["time_pref195"] == 1:
                            return 196
                        else:
                            return 194
                    else:
                        if d["time_pref185"] == 1:
                            return 186
                        else:
                            return 184
                else:
                    if d["time_pref170"] == 1:
                        if d["time_pref175"] == 1:
                            return 176
                        else:
                            return 174
                    else:
                        if d["time_pref165"] == 1:
                            return 166
                        else:
                            return 164


def risk_colval(*columns):
    for x in columns:
        if len(x) != len(columns)-1:
            continue
        
        d = x.to_dict()
        
        for k, v in d.items():
            val = int(re.findall("\d+", str(k))[0])
            if v == 3:
                return val

        if d["risk_pref240"] == 1:
            if d["risk_pref360"] == 1:
                if d["risk_pref420"] == 1:
                    if d["risk_pref450"] == 1:
                        if d["risk_pref465"] == 1:
                            return 466
                        else:
                            return 464
                    else:
                        if d["risk_pref435"] == 1:
                            return 436
                        else:
                            return 434
                else:
                    if d["risk_pref390"] == 1:
                        if d["risk_pref405"] == 1:
                            return 406
                        else:
                            return 404
                    else:
                        if d["risk_pref375"] == 1:
                            return 376
                        else:
                            return 374
            else:
                if d["risk_pref300"] == 1:
                    if d["risk_pref330"] == 1:
                        if d["risk_pref345"] == 1:
                            return 346
                        else:
                            return 344
                    else:
                        if d["risk_pref315"] == 1:
                            return 316
                        else:
                            return 314
                else:
                    if d["risk_pref270"] == 1:
                        if d["risk_pref285"] == 1:
                            return 286
                        else:
                            return 284
                    else:
                        if d["risk_pref255"] == 1:
                            return 256
                        else:
                            return 254
        else:
            if d["risk_pref120"] == 1:
                if d["risk_pref180"] == 1:
                    if d["risk_pref210"] == 1:
                        if d["risk_pref225"] == 1:
                            return 226
                        else:
                            return 224
                    else:
                        if d["risk_pref195"] == 1:
                            return 196
                        else:
                            return 194
                else:
                    if d["risk_pref150"] == 1:
                        if d["risk_pref165"] == 1:
                            return 166
                        else:
                            return 164
                    else:
                        if d["risk_pref135"] == 1:
                            return 136
                        else:
                            return 134
            else:
                if d["risk_pref60"] == 1:
                    if d["risk_pref90"] == 1:
                        if d["risk_pref105"] == 1:
                            return 106
                        else:
                            return 104
                    else:
                        if d["risk_pref75"] == 1:
                            return 76
                        else:
                            return 74
                else:
                    if d["risk_pref30"] == 1:
                        if d["risk_pref45"] == 1:
                            return 46
                        else:
                            return 44
                    else:
                        if d["risk_pref15"] == 1:
                            return 16
                        else:
                            return 14

def bayesian_calc(x):
    x = x.to_dict()
    goodnews, p1, p2, p3, p4 = x['goodnews'], x['prior_1'], x['prior_2'], x['prior_3'], x['prior_4']
    if p1 == 1:
        r1 = 1 if goodnews else 0
        r2 = 0 if goodnews else 1/3
        r3 = 0 if goodnews else 1/3
        r4 = 0 if goodnews else 1/3
    elif p4 == 1:
        r1 = 1/3 if goodnews else 0
        r2 = 1/3 if goodnews else 0
        r3 = 1/3 if goodnews else 0
        r4 = 0 if goodnews else 1
    else:
        r1 = (1*p1)/(1*p1 + (2/3)*p2 + (1/3)*p3 + 0*p4) if goodnews else 0
        r2 = ((2/3)*p2)/(1*p1 + (2/3)*p2 + (1/3)*p3 + 0*p4) if goodnews else ((1/3)*p2)/(0*p1 + (1/3)*p2 + (2/3)*p3 + 1*p4)
        r3 = ((1/3)*p3)/(1*p1 + (2/3)*p2 + (1/3)*p3 + 0*p4) if goodnews else ((2/3)*p3)/(0*p1 + (1/3)*p2 + (2/3)*p3 + 1*p4)
        r4 = 0 if goodnews else (1*p4)/(0*p1 + (1/3)*p2 + (2/3)*p3 + 1*p4)
    b_r = 1*r1 + 2*r2 + 3*r3 + 4*r4
    return b_r


def clean_data(r):
        # r.columns = r.columns.str.removeprefix("session.config.")
        r.columns = r.columns.str.removeprefix("mrt.1.player.")
        r = r.loc[r.loc[:,"participant.label"] < 25, 
                (~(r.columns.str.startswith("participant.")) & ~(r.columns.str.startswith("session.")))]

        r = r.loc[:, ~r.columns.isin(["role", "payoff", "inform1", "inform2", "inform3"])]
        r = r.loc[:, ~((r.columns.str.endswith("comp1")) | (r.columns.str.endswith("comp2")) | (r.columns.str.endswith("comp3")))]
        r = r.loc[:, ~(r.columns.str.startswith("mrt.") | (r.columns.str.startswith("pair_id")))]
        r = r.loc[:, ~r.columns.str.startswith("q")]
        r = r.loc[:, ~r.columns.isin(['id_in_group', 'time_pref_qual1', 'time_pref_qual2', 'random_bonus', 'prior_estimation_bonus', 'posterior_estimation_bonus', 'completion_fee', 'final_compensation'])]

        tp_cond = (r.columns.str.startswith("time_pref")) & (~r.columns.str.contains("qual"))
        tp = r.loc[:, tp_cond]
        temp = tp.apply(time_colval, axis=1, args=tuple(tp.columns))
        r = r.loc[:, ~tp_cond]
        r.loc[:,"time_pref"] = temp

        rp_cond = (r.columns.str.startswith("risk_pref")) & (~r.columns.str.contains("qual"))
        rp = r.loc[:, rp_cond]
        temp = rp.apply(risk_colval, axis=1, args=tuple(rp.columns))
        r = r.loc[:, ~rp_cond]
        r.loc[:,"risk_pref"] = temp

        del tp_cond, tp, rp_cond, rp, temp

        r.loc[:, r.columns.str.contains("(prior_\d+)|(posterior_\d+)")] = r.loc[:, r.columns.str.contains("(prior_\d+)|(posterior_\d+)")]/100
        r.loc[:, 'sat_act'] = r.loc[:, 'sat_act'].apply(lambda x: np.nan if x == 0 else x)
        r.loc[:, 'gpa'] = r.loc[:, 'gpa'].apply(lambda x: np.nan if x == 0 else x)
        r.loc[:, 'field_of_study'] = r.field_of_study.str.upper()

        r.loc[:, "rank_prior"] = (1*r.loc[:, 'prior_1'] + 2*r.loc[:, "prior_2"] + 3*r.loc[:, 'prior_3'] + 4*r.loc[:, "prior_4"]).astype(np.float)
        r.loc[:, "rank_posterior"] = (1*r.loc[:, 'posterior_1'] + 2*r.loc[:, "posterior_2"] + 3*r.loc[:, 'posterior_3'] + 4*r.loc[:, "posterior_4"]).astype(np.float)
        r.loc[:, "rank_bayesian"] = r.apply(bayesian_calc, axis=1)
        r.loc[:, "adjustment"] = (r.loc[:, "rank_posterior"] - r.loc[:, "rank_prior"]).astype(np.float)
        r.loc[:, "b_adjustment"] = (r.loc[:, "rank_bayesian"] - r.loc[:, "rank_prior"]).astype(np.float)
        return r