from otree.api import *
import random


doc = """
What motivates motivated beliefs?

Seura Ha (seura@umich.edu)
University of Michigan School of Information
Pre-candidacy milestone project
"""

# FUNCTIONS
def iq_questions():
    return models.IntegerField(
        label="Which cutout is the right completion?",
        choices = [[1, "A"],
                   [2, "B"],
                   [3, "C"],
                   [4, "D"]],
        widget=widgets.RadioSelectHorizontal,
    )

def risk_pref(sure_amount):
    return models.IntegerField(
        choices = [[1, "50/50 chance of getting $450 or getting nothing"],
                   [2, f"Sure payment of ${sure_amount}"],
                   [3, "I don't know"],],
        widget=widgets.RadioSelect,
        initial=99,
        label="",
    )


def time_pref(what_in_12):
    return models.IntegerField(
        choices = [[1, "$160 today"],
                   [2, f"${what_in_12} in 12 months"],
                   [3, "I don't know"],],
        widget=widgets.RadioSelect,
        initial=99,
        label="",
    )


def creating_session(subsession: BaseSubsession):
    subsession.group_randomly()
    players = subsession.get_players()
    for p in players:
        p.treatment = subsession.session.config['treatment']
        pair = p.group.get_player_by_id(5 - p.id_in_group)

        p.pair_id_in_session = pair.participant.id_in_session
        p.pair_id_in_group = 5 - p.id_in_group


# MODELS
class C(BaseConstants):
    NAME_IN_URL = 'mrt'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 1

    PIECE_RATE = 0.20
    RANDOM_BONUS_MAX = 100

    COMPLETION_FEE = 10


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    def score_rank_feedback(self):
        players = [p for p in self.get_players()]
        random.shuffle(players)
        players.sort(key=lambda p: p.iq_score)

        r = 4
        for p in players:
            p.rank = r
            r -= 1

        for p in players:
            pair = self.get_player_by_id(5 - p.id_in_group)
            p.goodnews = 1 if p.rank < pair.rank else 0



class Player(BasePlayer):
    treatment = models.StringField()

    # Comprehension quiz
    inform1 = models.IntegerField(
        label="1. How will you participate in the study?",
        choices=[[1, "By verbally communicating with other participants and answering survey questions on a paper"],
                 [2, "By performing tasks and answering questions on a computer screen"]],
        widget=widgets.RadioSelect,
    )

    inform2 = models.IntegerField(
        label="2. When will you get paid?",
        choices=[[1, "Today"],
                 [2, "10 days later"],
                 [3, "2 weeks later"]
                 ],
        widget=widgets.RadioSelect,
    )

    inform3 = models.IntegerField(
        label="3. How will you get paid?",
        choices=[[1, "You will be contacted by the Ross Paid Pool via email and click the link in the email to receive a gift card."],
                 [2, "You will come to this lab again and receive payment in cash"]],
        widget=widgets.RadioSelect,
    )

    belief_comp1 = models.IntegerField(
        label="1. Which of the following answers maximizes your chance of a payoff of 1 dollar?",
        choices=[[1, "A=25%, B=25%, C=25%, D=25%"],
                 [2, "A=50%, B=10%, C=15%, D=25%"],
                 [3, "A=50%, B=30%, C=15%, D=5%"],
                 [4, "A=100%, B=0%, C=0%, D=0%"]
                 ],
        widget=widgets.RadioSelect,
    )
    belief_comp2 = models.IntegerField(
        label="2. What is your chance to win 1 dollar?",
        choices=[[1, "25%"],
                 [2, "20%"],
                 [3, "15%"]],
        widget=widgets.RadioSelect,
    )
    belief_comp3 = models.IntegerField(
        label="3. Would you have had a higher chance of winning the 1 dollar by reporting 40% instead of 15%?",
        choices=[[1, "Yes"],
                 [2, "No"]],
        widget=widgets.RadioSelect,
    )

    prior_comp1 = models.IntegerField(
        label="1. You are randomly assigned into a group of ___ participants in this study. (Type in a number)"
    )
    prior_comp2 = models.IntegerField(
        label="2. [True or False] Your group members solved different problems than you.",
        choices=[[1, "True"],
                 [0, "False"]],
        widget=widgets.RadioSelectHorizontal
    )
    prior_comp3 = models.IntegerField(
        label="3. [True or False] Your task is to estimate the percentage chances with which you ranked 1st, 2nd, 3rd, 4th in the group.",
        choices=[[1, "True"],
                 [0, "False"]],
        widget=widgets.RadioSelectHorizontal
    )

    posterior_comp1 = models.IntegerField(
        label="1. [True or False] In Section 3, you will learn whether a randomly selected member of your group is higher or lower in rank than you.",
        choices=[[1, "True"],
                 [0, "False"]],
        widget=widgets.RadioSelectHorizontal
    )
    posterior_comp2 = models.IntegerField(
        choices=[[1, "True"],
                 [0, "False"]],
        widget=widgets.RadioSelectHorizontal,
        label="",
    )

    # IQ quiz
    q_warm_up = iq_questions()

    q1 = iq_questions()
    q2 = iq_questions()
    q3 = iq_questions()
    q4 = iq_questions()
    q5 = iq_questions()
    q6 = iq_questions()
    q7 = iq_questions()
    q8 = iq_questions()
    q9 = iq_questions()
    q10 = iq_questions()
    q11 = iq_questions()
    q12 = iq_questions()
    q13 = iq_questions()
    q14 = iq_questions()
    q15 = iq_questions()
    iq_score = models.IntegerField()
    rank = models.IntegerField()

    def score_calc(self):
        answers = [self.q1, self.q2, self.q3, self.q4, self.q5,
                   self.q6, self.q7, self.q8, self.q9, self.q10,
                   self.q11, self.q12, self.q13, self.q14, self.q15,]

        correct_answers = [2, 2, 3, 4, 1,
                           3, 2, 4, 1, 2,
                           4, 1, 3, 3, 4,]

        score = 0
        for i in range(15):
            if answers[i] == correct_answers[i]:
                score += 1
        self.iq_score = score


    # Belief elicitation, feedback
    prior_1 = models.IntegerField(min=0, max=100,
                                  label="Rank 1:")
    prior_2 = models.IntegerField(min=0, max=100,
                                  label="Rank 2:")
    prior_3 = models.IntegerField(min=0, max=100,
                                  label="Rank 3:")
    prior_4 = models.IntegerField(min=0, max=100,
                                  label="Rank 4:")

    pair_id_in_session = models.IntegerField()
    pair_id_in_group = models.IntegerField()
    goodnews = models.IntegerField()

    posterior_1 = models.IntegerField(min=0, max=100,
                                      label="Rank 1:")
    posterior_2 = models.IntegerField(min=0, max=100,
                                      label="Rank 2:")
    posterior_3 = models.IntegerField(min=0, max=100,
                                      label="Rank 3:")
    posterior_4 = models.IntegerField(min=0, max=100,
                                      label="Rank 4:")

    # Survey (Preferences)
    time_pref_qual1 = models.IntegerField(
        choices=[
            [0, "0: Does not describe me at all"],
            [1, "1"],
            [2, "2"],
            [3, "3"],
            [4, "4"],
            [5, "5"],
            [6, "6"],
            [7, "7"],
            [8, "8"],
            [9, "9"],
            [10, "10: Describes me perfectly"]
        ],
        widget=widgets.RadioSelect,
    )
    time_pref_qual2 = models.IntegerField(
        choices=[
            [0, "0: Completely unwilling to do so"],
            [1, "1"],
            [2, "2"],
            [3, "3"],
            [4, "4"],
            [5, "5"],
            [6, "6"],
            [7, "7"],
            [8, "8"],
            [9, "9"],
            [10, "10: Very willing to do so"]
        ],
        widget=widgets.RadioSelect,
    )

    risk_pref465 = risk_pref(465)
    risk_pref450 = risk_pref(450)
    risk_pref435 = risk_pref(435)
    risk_pref420 = risk_pref(420)
    risk_pref405 = risk_pref(405)
    risk_pref390 = risk_pref(390)
    risk_pref375 = risk_pref(375)
    risk_pref360 = risk_pref(360)
    risk_pref345 = risk_pref(345)
    risk_pref330 = risk_pref(330)
    risk_pref315 = risk_pref(315)
    risk_pref300 = risk_pref(300)
    risk_pref285 = risk_pref(285)
    risk_pref270 = risk_pref(270)
    risk_pref255 = risk_pref(255)
    risk_pref240 = risk_pref(240)
    risk_pref225 = risk_pref(225)
    risk_pref210 = risk_pref(210)
    risk_pref195 = risk_pref(195)
    risk_pref180 = risk_pref(180)
    risk_pref150 = risk_pref(150)
    risk_pref165 = risk_pref(165)
    risk_pref135 = risk_pref(135)
    risk_pref120 = risk_pref(120)
    risk_pref105 = risk_pref(105)
    risk_pref90 = risk_pref(90)
    risk_pref75 = risk_pref(75)
    risk_pref60 = risk_pref(60)
    risk_pref45 = risk_pref(45)
    risk_pref30 = risk_pref(30)
    risk_pref15 = risk_pref(15)

    time_pref343 = time_pref(343)
    time_pref336 = time_pref(336)
    time_pref329 = time_pref(329)
    time_pref323 = time_pref(323)
    time_pref316 = time_pref(316)
    time_pref309 = time_pref(309)
    time_pref303 = time_pref(303)
    time_pref296 = time_pref(296)
    time_pref290 = time_pref(290)
    time_pref283 = time_pref(283)
    time_pref277 = time_pref(277)
    time_pref270 = time_pref(270)
    time_pref264 = time_pref(264)
    time_pref258 = time_pref(258)
    time_pref252 = time_pref(252)
    time_pref246 = time_pref(246)
    time_pref240 = time_pref(240)
    time_pref234 = time_pref(234)
    time_pref228 = time_pref(228)
    time_pref223 = time_pref(223)
    time_pref217 = time_pref(217)
    time_pref212 = time_pref(212)
    time_pref206 = time_pref(206)
    time_pref201 = time_pref(201)
    time_pref195 = time_pref(195)
    time_pref190 = time_pref(190)
    time_pref185 = time_pref(185)
    time_pref180 = time_pref(180)
    time_pref175 = time_pref(175)
    time_pref170 = time_pref(170)
    time_pref165 = time_pref(165)


    # Survey (Demographics)
    age = models.IntegerField(
        label="How old are you?",
        min=15, max=95,
    )
    gender = models.IntegerField(
        label="What is your gender?",
        choices=[[1, "Female"],
                 [2, "Male"],
                 [3, "Non-binary / third gender"],
                 [4, "Prefer not to say"]],
        widget=widgets.RadioSelect,
    )
    field_of_study = models.StringField(
        label="Please indicate your field of study. If you have more than one field, please indicate the one you most identify with.",
    )
    sat_act = models.FloatField(
        label="What was your SAT/ACT score? If you do not want to share, write 0.",
        min=0,
    )
    gpa = models.FloatField(
        label="What is your current GPA? If you do not want to share, write 0.",
        min=0,
    )

    surveyIQ1 = models.IntegerField(
        label="1. Have you ever taken this kind of test before?",
        choices=[[1, "Yes"], [0, "No"]],
        widget=widgets.RadioSelectHorizontal,
    )
    surveyIQ2 = models.IntegerField(
        label="",
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelect,
        doc="Academic success"
    )
    surveyIQ3 = models.IntegerField(
        label="",
        choices=[1, 2, 3, 4, 5, 6, 7],
        widget=widgets.RadioSelect,
        doc="Professional success"
    )

    quiz_bonus = models.FloatField()
    random_bonus = models.FloatField()
    prior_estimation_bonus = models.FloatField()
    posterior_estimation_bonus = models.FloatField()
    completion_fee = models.FloatField(initial=C.COMPLETION_FEE)
    final_compensation = models.FloatField()

    def compensation_calc(self):
        self.quiz_bonus = self.iq_score*C.PIECE_RATE
        rn_max = C.RANDOM_BONUS_MAX
        self.random_bonus = random.randint(0, rn_max)/100

        rs = random.randint(1, 4)
        rs_p = [self.prior_1, self.prior_2, self.prior_3, self.prior_4][rs-1]
        rn = random.randint(0, 100)
        if rs_p >= rn:
            self.prior_estimation_bonus = 1 if rs == self.rank else 0
        else:
            if random.randint(0, 100) <= rn:
                self.prior_estimation_bonus = 1
            else:
                self.prior_estimation_bonus = 0

        rs = random.randint(1, 4)
        rs_p = [self.posterior_1, self.posterior_2, self.posterior_3, self.posterior_4][rs-1]
        rn = random.randint(0, 100)
        if rs_p >= rn:
            self.posterior_estimation_bonus = 1 if rs == self.rank else 0
        else:
            if random.randint(0, 100) <= rn:
                self.posterior_estimation_bonus = 1
            else:
                self.posterior_estimation_bonus = 0

        self.final_compensation = self.completion_fee + self.quiz_bonus + self.random_bonus + self.prior_estimation_bonus + self.posterior_estimation_bonus
        self.payoff = self.final_compensation # not accurate


# COMPREHENSION QUIZ FIELD VALIDATION
def belief_comp1_error_message(player, value):
    if value != 3:
        return 'You maximize your payoff when you give your best estimate.'

def belief_comp2_error_message(player, value):
    if value != 1:
        return 'According to the information on the leaflet, since 15% (your best estimate of the chance of C happening) ' \
               'is lower than the number X = 25%, ' \
               'you receive 1 dollar with a chance of 25%. '

def belief_comp3_error_message(player, value):
    if value != 2:
        return 'If you report 40% rather than 15%, you would have a lower chance of receiving 1 dollar. ' \
               'The information on the leaflet says that if your specified percentage chance ' \
               '(which is 40%) is at least as high as the number X ' \
               '(which is 25 in this example), then you receive a dollar ' \
               'if Scenario C has occurred. Note that in this example, ' \
               'you believe this case happens 15% of the time. ' \
               'Therefore, you will get a dollar with a 15% chance if you report 40%. \
               Instead, if you reported your best estimate of 15%, \
               then you get a dollar with 25% chance. Therefore, the chance of receiving \
               the additional payment is higher if you provide your best estimate.'

def prior_comp1_error_message(player, value):
    if value != 4:
        return 'There are 4 people in your group.'

def prior_comp2_error_message(player, value):
    if value != 0:
        return 'You and your group members solved the same questions.'

def prior_comp3_error_message(player, value):
    if value != 1:
        return 'You will estimate the percentage chances that you ranked 1st, 2nd, 3rd, and 4th in your group.'

def posterior_comp1_error_message(player, value):
    if value != 1:
        return 'You will learn whether a randomly selected member of your group \
        is higher or lower in rank than you.'

def posterior_comp2_error_message(player, value):
    if value != 1:
        return 'Please read the instruction above again and correct the answer to proceed.'

def inform1_error_message(player, value):
    if value != 2:
        return 'You will use a mouse and a keyboard to perform tasks and answer questions in a survey.'

def inform2_error_message(player, value):
    if value != 2:
        return 'The payment will be distributed 10 days later.'

def inform3_error_message(player, value):
    if value != 1:
        return 'The Ross Paid Pool will send you an email which \
        includes a link to the payment. The payment will be in the form of \
        a gift card of your choosing.'


# PAGES
class InformedConsent(Page):
    form_model="player"
    form_fields = ["inform1",
                   "inform2",
                   "inform3",
                   ]


class GeneralInstruction(Page):
    pass


class BeliefInstruction(Page):
    pass


class WaitforOthers(WaitPage):
    wait_for_all_groups = True

    body_text = "Please wait until the experiment continues."


class ControlQs(Page):
    form_model = "player"
    form_fields = ["belief_comp1",
                   "belief_comp2",
                   "belief_comp3"]


class OpeningSection1(Page):
    pass


class QuizInstruction(Page):
    pass


class Warmup(Page):
    form_model = "player"
    form_fields = ["q_warm_up"]

    timeout_seconds = 30


class WarmupResult(Page):
    pass


class Q1(Page):
    form_model = "player"
    form_fields = ["q1"]

    timeout_seconds = 30


class Q2(Page):
    form_model = "player"
    form_fields = ["q2"]

    timeout_seconds = 30


class Q3(Page):
    form_model = "player"
    form_fields = ["q3"]

    timeout_seconds = 30


class Q4(Page):
    form_model = "player"
    form_fields = ["q4"]

    timeout_seconds = 30


class Q5(Page):
    form_model = "player"
    form_fields = ["q5"]

    timeout_seconds = 30


class Q6(Page):
    form_model = "player"
    form_fields = ["q6"]

    timeout_seconds = 30


class Q7(Page):
    form_model = "player"
    form_fields = ["q7"]

    timeout_seconds = 30


class Q8(Page):
    form_model = "player"
    form_fields = ["q8"]

    timeout_seconds = 30


class Q9(Page):
    form_model = "player"
    form_fields = ["q9"]

    timeout_seconds = 30


class Q10(Page):
    form_model = "player"
    form_fields = ["q10"]

    timeout_seconds = 30


class Q11(Page):
    form_model = "player"
    form_fields = ["q11"]

    timeout_seconds = 30


class Q12(Page):
    form_model = "player"
    form_fields = ["q12"]

    timeout_seconds = 30


class Q13(Page):
    form_model = "player"
    form_fields = ["q13"]

    timeout_seconds = 30


class Q14(Page):
    form_model = "player"
    form_fields = ["q14"]

    timeout_seconds = 30


class Q15(Page):
    form_model = "player"
    form_fields = ["q15"]

    timeout_seconds = 30

    def before_next_page(player: Player, timeout_happened):
        player.score_calc()


class WaitAfterQuiz(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def after_all_players_arrive(subsession: BaseSubsession):
        for g in subsession.get_groups():
            g.score_rank_feedback()

    body_text = "Please wait until the experiment continues."


class OpeningSection2(Page):
    pass


class PriorInstruction(Page):
    form_model = "player"
    form_fields = ["prior_comp1",
                   "prior_comp2",
                   "prior_comp3"]


class Prior(Page):
    form_model = "player"
    form_fields = ["prior_1",
                   "prior_2",
                   "prior_3",
                   "prior_4"]

    @staticmethod
    def error_message(player, values):
        if values['prior_1'] + values['prior_2'] + values['prior_3'] + values['prior_4'] != 100:
            return 'The numbers must add up to 100.'

class OpeningSection3(Page):
    pass


class FeedbackInstruction(Page):
    form_model = "player"
    form_fields = ["posterior_comp1",
                   "posterior_comp2",]


class Feedback(Page):
    pass


class Posterior(Page):
    form_model = "player"
    form_fields = ["posterior_1",
                   "posterior_2",
                   "posterior_3",
                   "posterior_4"]

    @staticmethod
    def error_message(player, values):
        if values['posterior_1'] + values['posterior_2'] + values['posterior_3'] + values['posterior_4'] != 100:
            return 'The numbers must add up to 100.'

    def before_next_page(player: Player, timeout_happened):
        player.compensation_calc()


class OpeningSection4(Page):
    pass

class SurveyIQ(Page):
    form_model = "player"
    form_fields = ["surveyIQ1",
                   "surveyIQ2",
                   "surveyIQ3"
                   ]


class SurveyPrefQual1(Page):
    form_model = "player"
    form_fields = ["time_pref_qual1"]

class SurveyPrefQual2(Page):
    form_model = "player"
    form_fields = ["time_pref_qual2"]


class SurveyPrefRisk240(Page):
    form_model = "player"
    form_fields = ["risk_pref240"]


class SurveyPrefRisk360(Page):
    form_model = "player"
    form_fields = ["risk_pref360"]

    def is_displayed(player: Player):
        return player.risk_pref240 == 1


class SurveyPrefRisk120(Page):
    form_model = "player"
    form_fields = ["risk_pref120"]

    def is_displayed(player: Player):
        return player.risk_pref240 == 2


class SurveyPrefRisk420(Page):
    form_model = "player"
    form_fields = ["risk_pref420"]

    def is_displayed(player: Player):
        return player.risk_pref360 == 1


class SurveyPrefRisk300(Page):
    form_model = "player"
    form_fields = ["risk_pref300"]

    def is_displayed(player: Player):
        return player.risk_pref360 == 2


class SurveyPrefRisk450(Page):
    form_model = "player"
    form_fields = ["risk_pref450"]

    def is_displayed(player: Player):
        return player.risk_pref420 == 1


class SurveyPrefRisk390(Page):
    form_model = "player"
    form_fields = ["risk_pref390"]

    def is_displayed(player: Player):
        return player.risk_pref420 == 2


class SurveyPrefRisk465(Page):
    form_model = "player"
    form_fields = ["risk_pref465"]

    def is_displayed(player: Player):
        return player.risk_pref450 == 1


class SurveyPrefRisk435(Page):
    form_model = "player"
    form_fields = ["risk_pref435"]

    def is_displayed(player: Player):
        return player.risk_pref450 == 2


class SurveyPrefRisk330(Page):
    form_model = "player"
    form_fields = ["risk_pref330"]

    def is_displayed(player: Player):
        return player.risk_pref300 == 1


class SurveyPrefRisk270(Page):
    form_model = "player"
    form_fields = ["risk_pref270"]

    def is_displayed(player: Player):
        return player.risk_pref300 == 2


class SurveyPrefRisk345(Page):
    form_model = "player"
    form_fields = ["risk_pref345"]

    def is_displayed(player: Player):
        return player.risk_pref330 == 1


class SurveyPrefRisk315(Page):
    form_model = "player"
    form_fields = ["risk_pref315"]

    def is_displayed(player: Player):
        return player.risk_pref330 == 2


class SurveyPrefRisk285(Page):
    form_model = "player"
    form_fields = ["risk_pref285"]

    def is_displayed(player: Player):
        return player.risk_pref270 == 1


class SurveyPrefRisk255(Page):
    form_model = "player"
    form_fields = ["risk_pref255"]

    def is_displayed(player: Player):
        return player.risk_pref270 == 2


class SurveyPrefRisk180(Page):
    form_model = "player"
    form_fields = ["risk_pref180"]

    def is_displayed(player: Player):
        return player.risk_pref120 == 1


class SurveyPrefRisk60(Page):
    form_model = "player"
    form_fields = ["risk_pref60"]

    def is_displayed(player: Player):
        return player.risk_pref120 == 2


class SurveyPrefRisk210(Page):
    form_model = "player"
    form_fields = ["risk_pref210"]

    def is_displayed(player: Player):
        return player.risk_pref180 == 1


class SurveyPrefRisk150(Page):
    form_model = "player"
    form_fields = ["risk_pref150"]

    def is_displayed(player: Player):
        return player.risk_pref180 == 2


class SurveyPrefRisk225(Page):
    form_model = "player"
    form_fields = ["risk_pref225"]

    def is_displayed(player: Player):
        return player.risk_pref210 == 1


class SurveyPrefRisk195(Page):
    form_model = "player"
    form_fields = ["risk_pref195"]

    def is_displayed(player: Player):
        return player.risk_pref210 == 2


class SurveyPrefRisk165(Page):
    form_model = "player"
    form_fields = ["risk_pref165"]

    def is_displayed(player: Player):
        return player.risk_pref150 == 1


class SurveyPrefRisk135(Page):
    form_model = "player"
    form_fields = ["risk_pref135"]

    def is_displayed(player: Player):
        return player.risk_pref150 == 2


class SurveyPrefRisk90(Page):
    form_model = "player"
    form_fields = ["risk_pref90"]

    def is_displayed(player: Player):
        return player.risk_pref60 == 1


class SurveyPrefRisk30(Page):
    form_model = "player"
    form_fields = ["risk_pref30"]

    def is_displayed(player: Player):
        return player.risk_pref60 == 2


class SurveyPrefRisk105(Page):
    form_model = "player"
    form_fields = ["risk_pref105"]

    def is_displayed(player: Player):
        return player.risk_pref90 == 1


class SurveyPrefRisk75(Page):
    form_model = "player"
    form_fields = ["risk_pref75"]

    def is_displayed(player: Player):
        return player.risk_pref90 == 2


class SurveyPrefRisk45(Page):
    form_model = "player"
    form_fields = ["risk_pref45"]

    def is_displayed(player: Player):
        return player.risk_pref30 == 1


class SurveyPrefRisk15(Page):
    form_model = "player"
    form_fields = ["risk_pref15"]

    def is_displayed(player: Player):
        return player.risk_pref30 == 2


class SurveyPrefTime246(Page):
    form_model = "player"
    form_fields = ["time_pref246"]


class SurveyPrefTime296(Page):
    form_model = "player"
    form_fields = ["time_pref296"]

    def is_displayed(player: Player):
        return player.time_pref246 == 1


class SurveyPrefTime201(Page):
    form_model = "player"
    form_fields = ["time_pref201"]

    def is_displayed(player: Player):
        return player.time_pref246 == 2


class SurveyPrefTime323(Page):
    form_model = "player"
    form_fields = ["time_pref323"]

    def is_displayed(player: Player):
        return player.time_pref296 == 1


class SurveyPrefTime270(Page):
    form_model = "player"
    form_fields = ["time_pref270"]

    def is_displayed(player: Player):
        return player.time_pref296 == 2


class SurveyPrefTime336(Page):
    form_model = "player"
    form_fields = ["time_pref336"]

    def is_displayed(player: Player):
        return player.time_pref323 == 1


class SurveyPrefTime309(Page):
    form_model = "player"
    form_fields = ["time_pref309"]

    def is_displayed(player: Player):
        return player.time_pref323 == 2


class SurveyPrefTime283(Page):
    form_model = "player"
    form_fields = ["time_pref283"]

    def is_displayed(player: Player):
        return player.time_pref270 == 1


class SurveyPrefTime258(Page):
    form_model = "player"
    form_fields = ["time_pref258"]

    def is_displayed(player: Player):
        return player.time_pref270 == 2


class SurveyPrefTime343(Page):
    form_model = "player"
    form_fields = ["time_pref343"]

    def is_displayed(player: Player):
        return player.time_pref336 == 1


class SurveyPrefTime329(Page):
    form_model = "player"
    form_fields = ["time_pref329"]

    def is_displayed(player: Player):
        return player.time_pref336 == 2


class SurveyPrefTime316(Page):
    form_model = "player"
    form_fields = ["time_pref316"]

    def is_displayed(player: Player):
        return player.time_pref309 == 1


class SurveyPrefTime303(Page):
    form_model = "player"
    form_fields = ["time_pref303"]

    def is_displayed(player: Player):
        return player.time_pref309 == 2


class SurveyPrefTime290(Page):
    form_model = "player"
    form_fields = ["time_pref290"]

    def is_displayed(player: Player):
        return player.time_pref283 == 1


class SurveyPrefTime277(Page):
    form_model = "player"
    form_fields = ["time_pref277"]

    def is_displayed(player: Player):
        return player.time_pref283 == 2


class SurveyPrefTime264(Page):
    form_model = "player"
    form_fields = ["time_pref264"]

    def is_displayed(player: Player):
        return player.time_pref258 == 1


class SurveyPrefTime252(Page):
    form_model = "player"
    form_fields = ["time_pref252"]

    def is_displayed(player: Player):
        return player.time_pref258 == 2


class SurveyPrefTime223(Page):
    form_model = "player"
    form_fields = ["time_pref223"]

    def is_displayed(player: Player):
        return player.time_pref201 == 1


class SurveyPrefTime180(Page):
    form_model = "player"
    form_fields = ["time_pref180"]

    def is_displayed(player: Player):
        return player.time_pref201 == 2


class SurveyPrefTime234(Page):
    form_model = "player"
    form_fields = ["time_pref234"]

    def is_displayed(player: Player):
        return player.time_pref223 == 1


class SurveyPrefTime212(Page):
    form_model = "player"
    form_fields = ["time_pref212"]

    def is_displayed(player: Player):
        return player.time_pref223 == 2

class SurveyPrefTime240(Page):
    form_model = "player"
    form_fields = ["time_pref240"]

    def is_displayed(player: Player):
        return player.time_pref234 == 1


class SurveyPrefTime228(Page):
    form_model = "player"
    form_fields = ["time_pref228"]

    def is_displayed(player: Player):
        return player.time_pref234 == 2


class SurveyPrefTime217(Page):
    form_model = "player"
    form_fields = ["time_pref217"]

    def is_displayed(player: Player):
        return player.time_pref212 == 1


class SurveyPrefTime206(Page):
    form_model = "player"
    form_fields = ["time_pref206"]

    def is_displayed(player: Player):
        return player.time_pref212 == 2


class SurveyPrefTime190(Page):
    form_model = "player"
    form_fields = ["time_pref190"]

    def is_displayed(player: Player):
        return player.time_pref180 == 1


class SurveyPrefTime170(Page):
    form_model = "player"
    form_fields = ["time_pref170"]

    def is_displayed(player: Player):
        return player.time_pref180 == 2


class SurveyPrefTime195(Page):
    form_model = "player"
    form_fields = ["time_pref195"]

    def is_displayed(player: Player):
        return player.time_pref190 == 1


class SurveyPrefTime185(Page):
    form_model = "player"
    form_fields = ["time_pref185"]

    def is_displayed(player: Player):
        return player.time_pref190 == 2


class SurveyPrefTime175(Page):
    form_model = "player"
    form_fields = ["time_pref175"]

    def is_displayed(player: Player):
        return player.time_pref170 == 1


class SurveyPrefTime165(Page):
    form_model = "player"
    form_fields = ["time_pref165"]

    def is_displayed(player: Player):
        return player.time_pref170 == 2


class SurveyDemo(Page):
    form_model = "player"
    form_fields = ["age",
                   "gender",
                   "field_of_study",
                   "sat_act",
                   "gpa"
                   ]


class NowResult(Page):
    def is_displayed(player: Player):
        return player.treatment == "now"

    def vars_for_template(player: Player):
        if player.rank == 1:
            ro = "1st"
        elif player.rank == 2:
            ro = "2nd"
        elif player.rank == 3:
            ro = "3rd"
        else:
            ro = "4th"
        return dict(rank_ordinal=ro)


class Finished(Page):
    pass


page_sequence = [
    InformedConsent,
    WaitforOthers,
    GeneralInstruction,
    BeliefInstruction,
    # WaitforOthers,
    ControlQs, # wait for others
    WaitforOthers,
    OpeningSection1,
    QuizInstruction, # wait page
    WaitforOthers,
    Warmup, # wait page
    WarmupResult, # wait page
    WaitforOthers,
    Q1,
    Q2,
    Q3,
    Q4,
    Q5,
    Q6,
    Q7,
    Q8,
    Q9,
    Q10,
    Q11,
    Q12,
    Q13,
    Q14,
    Q15,
    WaitAfterQuiz,
    OpeningSection2,
    PriorInstruction, # wait page
    WaitforOthers,
    Prior, # wait page
    WaitforOthers,
    OpeningSection3,
    FeedbackInstruction, # wait page
    WaitforOthers,
    Feedback, # wait page
    WaitforOthers,
    Posterior, # wait page
    WaitforOthers,
    OpeningSection4,
    SurveyIQ,
    SurveyPrefQual1,
    SurveyPrefQual2,
    SurveyPrefRisk240,
    SurveyPrefRisk360,
    SurveyPrefRisk120,
    SurveyPrefRisk420,
    SurveyPrefRisk300,
    SurveyPrefRisk450,
    SurveyPrefRisk390,
    SurveyPrefRisk465,
    SurveyPrefRisk435,
    SurveyPrefRisk330,
    SurveyPrefRisk270,
    SurveyPrefRisk345,
    SurveyPrefRisk315,
    SurveyPrefRisk285,
    SurveyPrefRisk255,
    SurveyPrefRisk180,
    SurveyPrefRisk60,
    SurveyPrefRisk210,
    SurveyPrefRisk150,
    SurveyPrefRisk225,
    SurveyPrefRisk195,
    SurveyPrefRisk165,
    SurveyPrefRisk135,
    SurveyPrefRisk90,
    SurveyPrefRisk30,
    SurveyPrefRisk105,
    SurveyPrefRisk75,
    SurveyPrefRisk45,
    SurveyPrefRisk15,
    SurveyPrefTime246,
    SurveyPrefTime296,
    SurveyPrefTime201,
    SurveyPrefTime323,
    SurveyPrefTime270,
    SurveyPrefTime336,
    SurveyPrefTime309,
    SurveyPrefTime283,
    SurveyPrefTime258,
    SurveyPrefTime343,
    SurveyPrefTime329,
    SurveyPrefTime316,
    SurveyPrefTime303,
    SurveyPrefTime290,
    SurveyPrefTime277,
    SurveyPrefTime264,
    SurveyPrefTime252,
    SurveyPrefTime223,
    SurveyPrefTime180,
    SurveyPrefTime234,
    SurveyPrefTime212,
    SurveyPrefTime240,
    SurveyPrefTime228,
    SurveyPrefTime217,
    SurveyPrefTime206,
    SurveyPrefTime190,
    SurveyPrefTime170,
    SurveyPrefTime195,
    SurveyPrefTime185,
    SurveyPrefTime175,
    SurveyPrefTime165,
    SurveyDemo,
    NowResult,
    Finished
]
