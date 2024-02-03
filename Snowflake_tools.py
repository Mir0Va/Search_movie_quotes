###############################################################################################################################################
# This file contains tools to work with snowflake                                                                                             #
###############################################################################################################################################

import snowflake.connector
import os
from dotenv import load_dotenv
from snowflake.connector import DictCursor
import pandas as pd
from snowflake.connector.pandas_tools import write_pandas

load_dotenv()
PASSWORD  = os.getenv('SNOWSQL_PWD')
WAREHOUSE = os.getenv('WAREHOUSE')
ACCOUNT   = os.getenv("SNOWSQL_ACC")
USER      = os.getenv("SNOWSQL_USR")
DATABASE  = os.getenv("SNOWSQL_DB")
SCHEMA    = os.getenv("SNOWSQL_SCHEMA")

conn = snowflake.connector.connect(
    user      = USER,
    password  = PASSWORD,
    account   = ACCOUNT,
    warehouse = WAREHOUSE,
    database  = DATABASE,
    schema    = SCHEMA,
)

cur = conn.cursor(DictCursor)

def get_table(table_name="EMBEDDINGS"):
    '''
    This function returns a table. Mostly used for testing.
    
    Arguments:
    table_name:  the name of the table to search from the db.

    Retruns:     the table as a list of dictionaries.
    '''
    return cur.execute(f"SELECT * FROM {table_name}").fetchall()

def get_closest_embeddings(limit=3):
    '''
    This function returns the closest quotes to the embeddings in a table called SEARCH.
    
    Arguments:
    limit:       the amount of quotes that the function returns.

    Retruns:     quotes, movies and cosine similarity as a list of dictionares.
    '''
    
    closest = cur.execute(f'SELECT QUOTE, MOVIE, cosine_similarity(EMBEDDINGS, EMBD) AS score FROM EMBEDDINGS, SEARCH ORDER BY score DESC LIMIT {limit}')
    return closest.fetchall()

def create_table(df):
    '''
    Creates a table in SEARCH for a given df object.

    Arguments:
    df:          the DataFrame object for which the table is created.
    '''
    sucs, chunks, rows, out = write_pandas(
        conn=conn,
        table_name="SEARCH",
        df=df,
        schema="PUBLIC"
    )

def empty_table(table_name="SEARCH"):
    '''
    This function empties a table, but doesn't remove it.
    
    Arguments:
    table_name:  name of the table to be emptied.          
    '''
    cur.execute(f"TRUNCATE TABLE IF EXISTS {table_name}")

def do_embedding_search(search_df, limit=3):
    '''
    This function creates a temporary table for search, searches the closest elements and finally empties the temp table.
    
    Arguments:
    search_df:   the embeddings as a df.
    limit:       the amount of quotes that the function returns.

    Retruns:     quotes, movies and cosine similarity as a list of dictionares.
    '''
    create_table(search_df)
    closest = get_closest_embeddings(limit)
    empty_table()
    return closest

if __name__=="__main__":
    #embedding for hello world    
    emb = [-0.010025296360254288, -0.04359462484717369, 0.0003220057697035372, 0.03147032856941223, -0.05750967934727669, -0.01852404698729515, -0.0096876947209239, 0.05730418115854263, -0.0380462184548378, -0.039484694600105286, -0.009665677323937416, -0.02985571324825287, -0.008293253369629383, -0.034816987812519073, 0.020593689754605293, 0.020975327119231224, -0.05014115944504738, 0.015647094696760178, -0.0013907713582739234, 0.055542781949043274, 0.027375075966119766, -0.004377810284495354, -0.004168644547462463, -0.016982821747660637, 0.03922048583626747, 0.0012366488808766007, -0.030765770003199577, 0.036519672721624374, 0.015177387744188309, -0.05357588827610016, 0.04286070913076401, -0.037811364978551865, -0.007295127492398024, -0.011133509688079357, 0.008638194762170315, 0.004730090033262968, 0.005963069386780262, 0.020975327119231224, -0.023441284894943237, -0.015118674375116825, -0.027903495356440544, -0.023558711633086205, 0.033877573907375336, 0.02119550108909607, -0.058038096874952316, 0.026054026558995247, -0.0458550862967968, 0.026171453297138214, 0.036490317434072495, 0.05480886623263359, -0.026171453297138214, 0.005779590457677841, 0.015265458263456821, 0.09899062663316727, -0.0038897560443729162, -0.04095252603292465, 0.0013962757075205445, 0.07926295697689056, -0.03502248227596283, 0.002420088741928339, 0.02935665100812912, 0.018641473725438118, 0.014575576409697533, 0.007295127492398024, 0.017188318073749542, 0.009401467628777027, -0.038603994995355606, 0.007603372447192669, -0.012373828329145908, 0.05005308985710144, 0.0006105265929363668, 0.03226295858621597, -0.021371642127633095, -0.013254527933895588, -0.03913241624832153, -0.022237662225961685, -0.025701746344566345, 0.006674968171864748, -0.008351966738700867, -0.06035727262496948, -0.04306620731949806, 0.027066830545663834, -0.05237226560711861, -0.06299936771392822, -0.014384758658707142, -0.0019723998848348856, -0.02338257245719433, -0.0042530447244644165, -0.016307618468999863, -0.0037026074714958668, -0.003392527811229229, 0.017393814399838448, -0.03164646774530411, 0.014105870388448238, 0.02380824275314808, -0.012579324655234814, -0.022663334384560585, 0.04065896198153496, 0.06188381835818291, -0.021342284977436066, 0.02118082344532013, -0.030119923874735832, 0.034787628799676895, -0.015676451846957207, 0.029180509969592094, 0.00550437206402421, -0.004076904617249966, -0.025819173082709312, -0.031000623479485512, -0.008506089448928833, -0.14326044917106628, -0.00973172951489687, 0.021797312423586845, -0.016747968271374702, -0.0016375506529584527, 0.02118082344532013, 0.062470950186252594, -0.05005308985710144, 0.012359149754047394, -0.06840099394321442, 0.003142996458336711, 0.0032292315736413, -0.011940817348659039, -0.045179884880781174, -0.05108056962490082, -0.03240974247455597, -0.012689411640167236, 0.042126793414354324, -0.04576701670885086, 0.018876325339078903, 0.04532666876912117, 0.025643033906817436, 0.016234228387475014, -0.010905995965003967, -0.03942598029971123, 0.010406932793557644, -0.036431603133678436, -0.019639598205685616, -0.04286070913076401, 0.04350655525922775, 0.06305808573961258, -0.038603994995355606, -0.0061282007955014706, -0.03883884847164154, -0.01771673746407032, -0.039895687252283096, -0.008322610519826412, 0.022633977234363556, -0.02338257245719433, -0.005452997982501984, 0.039983756840229034, 0.04799812287092209, -0.04236164689064026, 0.020901935175061226, 0.02763928659260273, -0.018289193511009216, 0.023059649392962456, -0.0172470323741436, -0.012571985833346844, 0.016087444499135017, 0.034758273512125015, 0.03467020392417908, -0.04286070913076401, -0.007985008880496025, -0.0029301606118679047, -0.001267840270884335, -0.010869299992918968, -0.017012178897857666, -0.04785133898258209, -0.003598024370148778, 0.03813428804278374, 0.01730574481189251, -0.02035883627831936, -0.04218550771474838, -0.0045172544196248055, 0.01141973678022623, 0.015103996731340885, -0.06123797222971916, -0.008263897150754929, -0.042068079113960266, 0.03361336514353752, 0.057685818523168564, -0.00703458720818162, 0.007269440684467554, -0.045590877532958984, -0.021268893033266068, -0.015867268666625023, 0.024732977151870728, -0.012498593889176846, -0.009181292727589607, -0.05974078178405762, 0.06481948494911194, 0.03795814886689186, -0.01990380883216858, 0.026582445949316025, -0.03660774230957031, 0.06922297924757004, -0.003137491876259446, -0.0021870704367756844, 0.03748844191431999, 0.0047007338143885136, 0.008080418221652508, -0.045502807945013046, -0.02847595140337944, -0.023852277547121048, -0.06076826527714729, 0.000857305945828557, 0.07932166755199432, -0.011970174498856068, -0.04606058448553085, 0.07403746992349625, -0.011581198312342167, -0.03886820375919342, 0.006744690239429474, -0.02898969128727913, 0.01119222305715084, 0.0536639578640461, 0.016102122142910957, -0.005874999798834324, -0.03381885960698128, -0.049407243728637695, 0.06734415888786316, 0.06910555809736252, -0.018230479210615158, 0.045590877532958984, 0.0021265223622322083, -0.00042383663821965456, -0.013526076450943947, 0.048673324286937714, 0.012505932711064816, 0.015441598370671272, 0.014179262332618237, 0.025789817795157433, -0.028872264549136162, -0.004898890852928162, -0.004865864757448435, 0.03282073512673378, -0.010370236821472645, -0.0032604229636490345, 0.017555275931954384, -0.032615236937999725, 0.008175826631486416, 0.012395845726132393, 0.04567894712090492, 0.04286070913076401, -0.0211514662951231, -0.030853839591145515, -0.03147032856941223, 0.0020769829861819744, 0.04494503140449524, 0.02587788738310337, 0.03029606305062771, 0.005335571244359016, 0.004788803402334452, 0.027815425768494606, 0.008718925528228283, -0.00400718254968524, -0.0077721732668578625, 0.047322921454906464, -0.012850873172283173, -0.03205746039748192, -0.04532666876912117, -0.03402435779571533, -0.033906929194927216, -0.003227396635338664, -0.025290753692388535, -0.006939178332686424, -0.01013538334518671, -0.010920673608779907, -0.02812367118895054, 0.0474109910428524, -0.00010939939238596708, 0.06182510405778885, -0.01859743706882, -0.00243476708419621, 0.02074047364294529, -0.0032695969566702843, -0.009350093081593513, -0.020843220874667168, 0.0450037457048893, -0.03502248227596283, -0.006564880721271038, 0.013540755026042461, 0.029107118025422096, -0.05313553661108017, -0.0026439332868903875, 0.03966083377599716, -0.0051190657541155815, -7.3276947659906e-05, -0.013548093847930431, 0.02941536344587803, 0.057744529098272324, 0.03290880471467972, -0.017804808914661407, 0.007291458081454039, 0.011089474894106388, -0.0007440075860358775, -0.031793251633644104, 0.030971266329288483, -0.004612663760781288, 0.07943909615278244, -0.007882260717451572, 0.03672517091035843, 0.014333384111523628, 0.009056526236236095, 0.03593254089355469, 0.02326514571905136, -0.03927919641137123, 0.06059212610125542, 0.0009650998981669545, -0.016689255833625793, -0.007647407241165638, 0.0579206719994545, -0.02460087276995182, -0.010076669976115227, -0.03969019278883934, 0.0018623125506564975, -0.024909118190407753, 0.005133744329214096, -0.04835040122270584, 0.03405371308326721, -0.056394126266241074, -0.01013538334518671, -0.029048405587673187, 0.014773733913898468, -0.015779199078679085, 0.061061833053827286, -0.005658494308590889, -0.006410758476704359, -0.008535445667803288, 0.024351341649889946, -0.02545221522450447, -0.010267488658428192, 0.0004130572488065809, 0.00444753235206008, -0.015867268666625023, -0.019243285059928894, 0.04497438669204712, 0.0010999570367857814, 0.048174262046813965, -0.028402559459209442, -0.017569955438375473, 0.010663802735507488, -0.012975639663636684, 0.0026787943206727505, 0.004194331355392933, 0.05102185904979706, -0.018846970051527023, -0.0076253898441791534, 0.0003233818570151925, -0.017129605636000633, -0.0038163645658642054, 0.01145643275231123, -0.024732977151870728, -0.013599468395113945, -0.017613990232348442, 0.0519612692296505, -0.0189497172832489, -0.003087952733039856, 0.025598999112844467, -0.011375701986253262, -0.027360398322343826, -0.008337289094924927, -0.0018311210442334414, 0.03323172777891159, 0.009665677323937416, -0.004275062121450901, -0.04594315588474274, 0.003544815583154559, 0.031000623479485512, -0.0012650880962610245, 0.009012491442263126, 0.031000623479485512, -0.019757024943828583, -0.0387507788836956, -0.029459398239850998, 0.0276099294424057, -0.004608993884176016, 0.055073074996471405, 0.008051061071455479, 0.029077762737870216, 0.004021861124783754, -0.015632417052984238, -0.027507180348038673, 0.010238131508231163, -0.0173204243183136, 0.01726171001791954, 0.004612663760781288, -0.00703458720818162, 0.002680629026144743, 0.050346653908491135, -0.008704246953129768, 0.011280292645096779, 0.010377575643360615, -0.0006912573589943349, -0.0034604151733219624, -0.005695190280675888, -0.018054340034723282, -0.02207620069384575, -0.04999437555670738, 0.044211115688085556, -0.02507057972252369, 0.017496563494205475, -0.0034200497902929783, -0.04623672366142273, -0.03511055186390877, 0.0066529507748782635, 0.058008741587400436, 0.010751873254776001, -0.028241097927093506, 0.003640224691480398, -0.054544657468795776, 0.03919112682342529, 0.02758057229220867, -0.01906714402139187, -0.0001553838374093175, -0.030883196741342545, -0.03270330652594566, 0.002867777831852436, -0.00712632667273283, 0.013129761442542076, 0.023397250100970268, -0.01635165326297283, 0.028593378141522408, -0.01771673746407032, 0.0370480939745903, 0.0388975627720356, -0.02681729942560196, 0.0125646460801363, -0.05489693582057953, -0.0032255619298666716, -0.022296376526355743, -0.010150061920285225, 0.026259522885084152, -0.007603372447192669, -0.052489690482616425, -0.011757338419556618, -0.012770142406225204, 0.035257335752248764, 0.02633291482925415, 0.0033650060649961233, -0.0030604307539761066, 0.02373485080897808, 0.010810586623847485,
            -0.0036273810546845198, -0.03487570211291313, -0.016204871237277985, -0.024351341649889946, -0.015338849276304245, 0.001704520545899868, 0.023646781221032143, -0.07127794623374939, 0.017437851056456566, 0.022780761122703552, 0.0017935078358277678, -0.00027040226268582046, 0.014406776055693626, 0.016513114795088768, -0.00222376617603004, 0.01645440235733986, -0.005772251170128584, 0.008939100429415703, -0.054163020104169846, 0.03980761766433716, 0.0146930031478405, -0.005067691672593355, -0.010957369580864906, 0.024072453379631042, -0.021679885685443878, -0.03599125146865845, -0.016601186245679855, 0.010641785338521004, 0.010810586623847485, -0.028387879952788353, -0.03202810510993004, -0.020960647612810135, -0.025598999112844467, 0.00637406250461936, -0.04289006441831589, -0.005427310708910227, 0.02812367118895054, 0.003768659895285964, 0.015691129490733147, 0.027477825060486794, 0.01764334738254547, 0.04136351868510246, -0.0713953748345375, 0.0038677386473864317, -0.035668328404426575, -0.011067457497119904, -0.04623672366142273, 0.06059212610125542, 0.04309556260704994, -0.017848843708634377, -0.014318706467747688, -0.03205746039748192, 0.00409158319234848, -0.017129605636000633, 0.0027797077782452106, -0.026127418503165245, 0.022369766607880592, -0.026465019211173058, 6.897666025906801e-05, 0.013460024259984493, 0.04523859918117523, -0.005317223258316517, -0.05128606781363487, -0.016336975619196892, 0.021048719063401222, -0.044328540563583374, -0.05651155114173889, 0.010737194679677486, -0.003744807792827487, -0.02805027924478054, 0.013672859407961369, -0.003383353818207979, 0.008271235972642899, 0.015412241220474243, -0.010201435536146164, -0.011955495923757553, 0.02507057972252369, 0.035198625177145004, -0.008168487809598446, -0.02851998619735241, 0.022267019376158714, 0.016263583675026894, -0.04101124033331871, -0.025378823280334473, -0.012975639663636684, 0.028329167515039444, 0.010957369580864906, -0.013423328287899494, 0.02806495688855648, 0.006440115161240101, -0.013107744045555592, -0.015588381327688694, -0.015426919795572758, 0.014333384111523628, -0.01853872463107109, -0.020402871072292328, 0.006212600972503424, 0.026098061352968216, 0.013555433601140976, 0.015911303460597992, -0.0254815723747015, 0.00969503354281187, 0.0387507788836956, -0.0003013643727172166, -0.0048585254698991776, 0.038574639707803726, 0.0189497172832489, -0.01641036756336689, -0.02078450843691826, -0.016542471945285797, 0.030031852424144745, 0.004656698554754257, -0.021063396707177162, -0.010861960239708424, 0.005687850993126631, 0.049876946955919266, 0.03023734875023365, 0.0011394049506634474, 0.02554028481245041, 0.02468894235789776, -0.0033099623396992683, 0.028710803017020226, -0.0016375506529584527, -0.03161711245775223, -0.041686441749334335, -0.05533728376030922, -0.023089004680514336, -0.033055588603019714, -0.01686539500951767, -0.05753903463482857, 0.027052152901887894, -1.5954077753121965e-05, 0.02034415863454342, 0.007265770807862282, 0.004895221441984177, -0.011221579276025295, -0.010876638814806938, -0.01592598296701908, -0.013019674457609653, 0.019654277712106705, -0.05615927278995514, 0.04629543796181679, 0.014164583757519722, 0.014105870388448238, 0.013078387826681137, -0.03243909776210785, 0.0049209087155759335, 0.014171922579407692, 0.011155527085065842, 0.0536639578640461, -0.024321984499692917, -0.03675452619791031, -0.010260148905217648, -0.003484267508611083, -0.029224544763565063, 0.020549654960632324, 0.020843220874667168, 0.004242036025971174, -0.008366645313799381, -0.045620232820510864, 0.011962834745645523, -0.016248906031250954, -0.024747656658291817, -0.0043631321750581264, 0.004594315774738789, -0.039895687252283096, -0.02551092952489853, 0.034259211272001266, -0.02203216589987278, -0.0518144890666008, -0.013254527933895588, 0.03616739436984062, -0.010861960239708424, 0.018773578107357025, -0.009276701137423515, -0.03144097328186035, -0.006792394910007715, -0.06564147025346756, -0.005023656878620386, 0.018670829012989998, -0.005163101013749838, 0.018406620249152184, -0.009328075684607029, -0.005280527286231518, -0.018435975536704063, 0.011537163518369198, 0.027786068618297577, 0.008784977719187737, 0.02154778130352497, -0.005254840478301048, -0.013540755026042461, -0.002370549598708749, -0.0030641003977507353, -0.01296829991042614, -0.019096501171588898, -0.02294222265481949, 0.039455339312553406, 0.008564802818000317, 0.017144283279776573, -0.03402435779571533, 0.046500932425260544, 0.02467426471412182, 0.014949874021112919, 0.022780761122703552, 0.011177544482052326, -0.0033796844072639942, 0.025613676756620407, 0.021900061517953873, 0.019727669656276703, 0.005735555663704872, 0.01642504520714283, -0.01186742540448904, -0.02241380326449871, -0.019199248403310776, -0.04156901687383652, 0.011265614069998264, -0.00863085500895977, 0.08002623170614243, -0.020094627514481544, -0.005034665577113628, -0.025819173082709312, 0.006730012129992247, -0.0164690800011158, 0.017511241137981415, -0.016557151451706886, -0.0013513233279809356, -0.003798016579821706, -0.00027040226268582046, 0.04377076402306557, -0.00840334128588438, 0.03405371308326721, -0.0029136475641280413, -0.02206152305006981, -0.02421923726797104, -8.227889338741079e-05, -0.024865083396434784, 0.024321984499692917, 0.013775608502328396, -0.036490317434072495, -0.028387879952788353, -0.0006885051843710244, 0.0076620858162641525, 0.004777794703841209, 0.017144283279776573, -0.006854777690023184, 0.002188905142247677, -0.030912552028894424, -0.023632103577256203, -0.012850873172283173, 0.024938473477959633, -0.00990786962211132, -0.05278325825929642, 0.013327918946743011, -0.010289506055414677, -0.01039225421845913, -0.04309556260704994, 0.0272576492279768, -0.015911303460597992, -0.016718612983822823, 0.011625233106315136, 0.0020678089931607246, -0.015514989383518696, -0.010597750544548035, 0.014582916162908077, 0.03405371308326721, 0.0031650138553231955, -0.03933791071176529, 0.002937499899417162, -0.03977826237678528, 0.0008765712263993919, -0.05748032033443451, -0.003764990484341979, -0.030795125290751457, -0.04177451133728027, 0.010722516104578972, 0.003744807792827487, -0.038193002343177795, 0.006939178332686424, -0.021518424153327942, 0.0049209087155759335, -0.011537163518369198, -0.017437851056456566, 0.003922782372683287, -0.011038100346922874, 0.020168019458651543, 0.017056213691830635, 0.02069643884897232, -0.01251327246427536, 0.006810742896050215, 0.02545221522450447, 0.003783338237553835, -0.004777794703841209, -0.04089381545782089, -0.01729106716811657, 0.008197844959795475, -0.030442846938967705, -0.03229231387376785, 0.020109305158257484, 0.029899748042225838, 0.01340864971280098, -0.003966817166656256, -0.002935664961114526, 0.007192379329353571, 0.012865551747381687, -0.030971266329288483, 0.0114637715741992, 0.0046677072532474995, 0.012447219341993332, -0.03370143473148346, -0.00840334128588438, 0.008241879753768444, -0.012799499556422234, 0.01729106716811657, 0.002240279456600547, -0.017026856541633606, 0.017599312588572502, -0.008528106845915318, 0.022678012028336525, -0.004076904617249966, 0.04796876758337021, -0.014883821830153465, 0.01811305247247219, 0.02294222265481949, 0.008586820214986801, -0.005750233773142099, 0.007265770807862282, 0.04015989601612091, -0.005687850993126631, 0.014105870388448238, 0.003032909007743001, -0.0009485867340117693, 0.005258509889245033, -0.037371017038822174, 0.012021548114717007, -0.022751403972506523, -0.016703933477401733, -0.021489067003130913, -0.000656396325211972, -0.01467832550406456, -0.009643659926950932, 0.017613990232348442, -0.024732977151870728, 0.002511828439310193, -0.001348571153357625, 0.02595127932727337, -0.04236164689064026, -0.04101124033331871, -0.0272576492279768, -0.005328231956809759, -0.011691286228597164, 0.013327918946743011, 0.06082697957754135, -0.016674578189849854, -0.026083383709192276, 0.013555433601140976, 0.004722751211374998, 0.005779590457677841, -0.036049965769052505, 0.030325420200824738, 0.03358400613069534, -0.005467676091939211, -0.003513623960316181, -0.016557151451706886, 0.0036805900745093822, -0.0030696047469973564, -0.004164974670857191, 0.010913334786891937, 0.042567141354084015, -0.010553715750575066, -0.01557370275259018, 0.009005152620375156, -0.03813428804278374, 0.012638038024306297, -0.012850873172283173, 0.03029606305062771, -0.00215587904676795, 0.028784194961190224, 0.002194409491494298, -0.032644595950841904, -0.016968144103884697, 0.062353525310754776, 0.015162710100412369, -0.01893503963947296, 0.034376636147499084, 0.01490583922713995, -0.01815708726644516, -0.01853872463107109, 0.004223688039928675, -0.019228605553507805, -0.009775764308869839, 0.014113209210336208, 0.025643033906817436, 0.007309806067496538, -0.01602873019874096, -0.01862679421901703, -0.011485788971185684, 0.006550202611833811, -0.009665677323937416, -0.0011513311183080077, -0.012704090215265751, 0.03813428804278374, -0.02674390748143196, 0.013232509605586529, -0.01635165326297283, -0.0009605129016563296, 0.015485633164644241, -0.023573389276862144, -0.021518424153327942, 0.012902247719466686, -0.011353684589266777, -0.03593254089355469, 0.01058307196944952, -0.027477825060486794, -0.0004155800852458924, 0.0003754440404009074, -0.03467020392417908, -0.0061979228630661964, 0.03211617469787598, 0.016924109309911728, 0.0048144906759262085, 0.038193002343177795, -0.012549967505037785, 0.01685071736574173, -0.007133665960282087, 0.03913241624832153, 0.04409368708729744, 0.004469550214707851, -0.006597907282412052, -0.0025191674940288067, -0.020388193428516388, 0.020123982802033424, 0.05049343779683113, -0.06294065713882446, 0.03710680454969406, -0.013709555380046368, -0.02022673189640045, 0.03141161426901817, 0.03505184128880501, 0.006840099580585957, -0.005838303826749325, -0.02289818786084652, -0.025687068700790405, -0.004502576310187578,
            0.01897907443344593, 0.01943410187959671, -0.0014320540940389037, -0.016718612983822823, 0.008131791837513447, -0.0073648495599627495, -0.01423797570168972, -0.007504293695092201, -0.0010687655303627253, 0.0006752029294148088, 0.03684259578585625, 0.012946282513439655, 0.012777482159435749, 0.0027448467444628477, -0.010465646162629128, 0.013225170783698559, 0.032556526362895966, 0.01013538334518671, -0.006641942076385021, 0.007764833979308605, 0.0021577137522399426, 0.009041848592460155, 0.0016632376937195659, -0.006553872022777796, -0.043858833611011505, 0.030501559376716614, 0.010003278963267803, 0.05316489189863205, 0.015749841928482056, -0.00026420984067954123, 0.027477825060486794, -0.0011916965013369918, 0.006645611487329006, -0.019551528617739677, -0.05560149624943733, -0.014832447282969952, 0.012689411640167236, -0.023191753774881363, 0.010047313757240772, -0.027815425768494606, 0.06787257641553879, 0.01688007451593876, -0.0014971891650930047, 0.025687068700790405, 0.014157244935631752, -0.02849062904715538, 0.015867268666625023, 0.012256401591002941, -0.02245783805847168, -0.05008244514465332, 0.029635537415742874, -0.006447454448789358, -0.02628888003528118, -0.03766458109021187, 0.014986569993197918, 0.006480480544269085, -0.008645533584058285, 0.06211867183446884, 0.01339397206902504, 0.015162710100412369, 0.009790442883968353, -0.00884369108825922, -0.012454559095203876, -0.014854464679956436, 0.006047470029443502, -0.0013173796469345689, 0.0001331370003754273, -0.026054026558995247, 0.015470954589545727, 0.046001870185136795, -0.0082345400005579, -0.013988443650305271, 0.00595206068828702, -0.010061991401016712, -0.015118674375116825, -0.01850936748087406, -0.013129761442542076, -0.013907712884247303, -0.011970174498856068, -0.034758273512125015, -0.016542471945285797, 0.00453193299472332, 0.0052621797658503056, -0.002675124676898122, 0.0013008665991947055, 0.045179884880781174, 0.012447219341993332, 0.0009160191984847188, -0.0023980713449418545, -0.026509055867791176, 0.03243909776210785, 0.03845721110701561, 0.008124453015625477, 0.01252061128616333, 0.004352123476564884, 0.021474389359354973, -0.017613990232348442, -0.010495002381503582, 0.009115239605307579, 0.02075515128672123, 0.005100717768073082, -0.019169893115758896, -0.019111178815364838, 0.01057573314756155, -0.01163257285952568, -0.03831042721867561, 0.026465019211173058, 0.04242036119103432, -0.02024140954017639, -0.028652090579271317, -0.013291222974658012, -0.027448467910289764, -0.014604933559894562, 0.020857900381088257, 0.018773578107357025, 0.016219548881053925, 0.013929730281233788, 0.022105557844042778, 0.0034952762071043253, -0.005148422438651323, 0.01122891902923584, -0.0013623320264741778, 0.006278653629124165, 0.016498437151312828, -0.0002802642702590674, -0.02932729385793209, 0.021459711715579033, 0.019580885767936707, 0.00994456559419632, -0.024732977151870728, 0.028373202309012413, -0.011280292645096779, -0.00018554320558905602, -0.010935352183878422, -0.012777482159435749, 0.002667785622179508, -0.003258588258177042, -0.014149905182421207, -0.018289193511009216, 0.010340879671275616, -0.012887569144368172, -0.012726107612252235, 0.028270453214645386, -0.014487506821751595, 0.02025608904659748, -0.006029122043401003, 0.023955026641488075, -0.00035663743619807065, 0.036108680069446564, -0.02245783805847168, -0.0207257941365242, -0.021312927827239037, -0.005280527286231518, -0.008931760676205158, -0.010869299992918968, -0.011250936426222324, 0.023030292242765427, 0.004168644547462463, -0.0024237583857029676, -0.02979700081050396, 0.021782634779810905, -0.00475944671779871, -0.006436445750296116, -0.007904278114438057, 0.017364459112286568, -0.01016474049538374, 0.029048405587673187, 0.020520297810435295, 0.027022795751690865, 0.012843534350395203, -0.00743090221658349, 0.0005742894718423486, 0.011111492291092873, -0.04882010817527771, -0.029620859771966934, -0.04744034633040428, 0.009401467628777027, 0.016190191730856895, -0.01168394647538662, 0.03235102817416191, 0.01947813667356968, 0.008249218575656414, 0.020828543230891228, -0.029708929359912872, 0.014377419836819172, -0.01604340970516205, 0.026083383709192276, -0.009489537216722965, -0.009540911763906479, 0.030971266329288483, -0.033466581255197525, 0.017878200858831406, -0.0004701651050709188, 0.021518424153327942, -0.0032604229636490345, 0.025628356263041496, -0.020168019458651543, -0.028637412935495377, -0.022751403972506523, 0.013643503189086914, -0.004719081334769726, 0.011258275248110294, 0.002280644839629531, 0.014634289778769016, 0.005695190280675888, -0.030046531930565834, -0.0005041087279096246, -0.03698937967419624, 0.01940474659204483, 0.011441754177212715, 0.011713303625583649, 0.04189193993806839, -0.017511241137981415, -0.0018916691187769175, 0.018347905948758125, 0.009181292727589607, -0.0004591563483700156, 0.001498106517829001, 0.013078387826681137, -0.013298562727868557, -0.007056604605168104, -0.01770205982029438, 0.0346408486366272, 0.017834164202213287, -0.0029154822696000338, 0.0005426393472589552, 0.002515497850254178, 0.014626950956881046, -0.0051117269322276115, -0.018729543313384056, -0.00888772588223219, 0.008638194762170315, -0.004344784189015627, 0.022208305075764656, -0.030795125290751457, 0.020843220874667168, -0.007298797369003296, 0.0009972087573260069, 0.014076514169573784, 0.047675199806690216, 0.028373202309012413, -0.03555090352892876, -0.00014471911708824337, 0.016483759507536888, 0.01212429627776146, 0.02160649374127388, -0.045150529593229294, 0.009342754259705544, 0.04535602405667305, -0.02552560716867447, -0.012505932711064816, -0.03240974247455597, 0.018876325339078903, 0.03599125146865845, -0.006425436586141586, -0.005001639481633902, -0.01122891902923584, -0.04409368708729744, -0.013071048073470592, 0.008491410873830318, 0.12764272093772888, -0.01141973678022623, -0.03696002438664436, 0.012249061837792397, 0.023910991847515106, -0.019712990149855614, -0.004807151388376951, 0.007174031343311071, 0.011324327439069748, -0.006330027710646391, -0.011324327439069748, -0.02932729385793209, -0.042156148701906204, 0.002812734106555581, -0.008616176433861256, 0.013606807217001915, -0.007419893518090248, -0.034816987812519073, -0.010649125091731548, -0.009988600388169289, 0.015705807134509087, -0.03924984112381935, -0.005761242471635342, 0.011801373213529587, -0.006524515338242054, -0.026465019211173058, -0.03017863631248474, -0.019272640347480774, 0.008293253369629383, 0.05316489189863205, -0.0061318702064454556, 0.0047044032253324986, 0.037723295390605927, -0.004190661944448948, 0.005023656878620386, 0.048673324286937714, -0.028358524665236473, -0.03831042721867561, -0.03352529555559158, 0.01859743706882, -0.03114740550518036, 0.0056401463225483894, 0.025158649310469627, -0.017452528700232506, -0.006561211310327053, -0.0013907713582739234, -0.003453075885772705, -0.0168213602155447, -0.002445776015520096, -0.011111492291092873, -0.02755121700465679, 0.03135290369391441, 0.007632729131728411, 0.015250779688358307, 0.01167660765349865, -0.00991520844399929, 0.04403497651219368, 0.04406433179974556, 0.05974078178405762, -0.009621642529964447, -0.007111648563295603, 0.008528106845915318, 0.01358478982001543, 0.027008118107914925, 0.009085883386433125, -0.005684181582182646, -0.0329381600022316, 0.032967519015073776, -0.009460180066525936, 0.041627731174230576, -0.007764833979308605, 0.029635537415742874, 0.016689255833625793, 0.02943004108965397, 0.020476263016462326, 0.029518112540245056, -0.021723920479416847, 0.01013538334518671, -0.00885102991014719, 0.0190231092274189, -0.014832447282969952, -0.020608369261026382, 0.016703933477401733, 0.02411648817360401, 0.012630698271095753, 0.02455683797597885, 0.0074052149429917336, 0.010450967587530613, -0.01598469540476799, -0.011126170866191387, 0.00462367245927453, -0.01145643275231123, 0.026068706065416336, 0.0065024979412555695, -0.001759564271196723, 0.02421923726797104, -0.04691192880272865, 0.00296685635112226, -0.006330027710646391, 0.02546689473092556, 0.009364771656692028, 0.029121797531843185, 0.008043722249567509, 0.02504122257232666, -0.01552966795861721, -0.009650998748838902, 0.003247579326853156, -0.047352276742458344, -0.04782198369503021, 0.01594066061079502, 0.008322610519826412, -0.00946751981973648, 0.010957369580864906, 0.015735164284706116, 0.05172641575336456, -0.059799496084451675, -0.04318363219499588, -0.03061898611485958, 0.003687929129227996, 0.008506089448928833, 0.06123797222971916, 0.02586320787668228, 0.014560898765921593, -0.015705807134509087, 0.040835101157426834, 0.0012256401823833585, 0.05225483700633049, 0.027463145554065704, 0.03754715621471405, -0.017012178897857666, -0.008770299144089222, -0.009871173650026321, 0.006227279547601938, 0.014781073667109013, 0.005563085433095694, 0.001714611891657114, 0.01014272216707468, -0.02376420795917511, -0.013959087431430817, 0.0061979228630661964, -0.010296844877302647, -0.02762460708618164, 0.011030761525034904, -0.011977513320744038, -0.022780761122703552, -0.00010681921412469819, 0.03023734875023365, -0.017599312588572502, -0.030149279162287712, -0.04931917041540146, -0.015632417052984238, -0.019199248403310776, 0.020843220874667168, -0.013995783403515816, 0.002711820648983121, -0.0030494220554828644, -0.02806495688855648, -0.006084165535867214, 0.002983369631692767, -0.03813428804278374, -0.048966892063617706, -0.003247579326853156, 0.001088030869141221, -0.0014696673024445772, -0.009005152620375156, 0.010010617785155773, -0.02248719334602356, 0.011067457497119904, -0.013100405223667622, -0.0045576198026537895, 0.015074639581143856, -0.02940068580210209, -0.008124453015625477, 0.020388193428516388, 0.017408493906259537, -0.02074047364294529, 0.010722516104578972, 0.0056401463225483894, 0.031264834105968475, -0.0037796685937792063, -0.04914303123950958, -0.030472202226519585, 0.023955026641488075, -0.008520768024027348,
              -0.01447282824665308, 0.027947530150413513, -0.016938786953687668, -0.008718925528228283, -0.008814333938062191, -0.032644595950841904, -0.0015779199311509728, -0.02291286550462246, -0.0024531150702387094, -0.01595534011721611, 0.001478841295465827, -0.02330918051302433, -0.026978760957717896, -0.04494503140449524, 0.005735555663704872, 0.0011907791486009955, -0.03196939080953598, -0.007309806067496538, 0.02074047364294529, 0.00433744490146637, 0.021503746509552002, 0.010744533501565456, -0.02024140954017639, 0.016146156936883926, -0.008476732298731804, -0.011148188263177872, -0.0003197122714482248, 0.023221110925078392, 0.01186742540448904, 0.001638468005694449, 0.043036848306655884, 0.06581760942935944, -0.01425265334546566, 0.030765770003199577, 0.011984852142632008, -0.005911695305258036, 0.00701623922213912, -0.002150374697521329, 0.0329381600022316, -0.025687068700790405, -0.0023632103111594915, 0.016630541533231735, -0.0076620858162641525, -0.013907712884247303, -0.01862679421901703, -0.00614654878154397, 0.026186132803559303, 0.020094627514481544, 0.031294189393520355, 0.04632479324936867, -0.01599937491118908, 0.013012335635721684, 0.010876638814806938, 0.0005036500515416265, 0.003823703620582819, -0.009232666343450546, -0.017423171550035477, -0.008682229556143284, -0.0029998826794326305, -0.010715177282691002, -0.0030090566724538803, 0.047264207154512405, 0.030883196741342545, -0.01818644441664219, 0.013100405223667622, -0.005849312525242567, -0.0018714864272624254, 0.03499312698841095, -0.028299810364842415, -0.017599312588572502, -0.007574015762656927, -0.005328231956809759, 0.011801373213529587, 0.002928325906395912, 0.015001248568296432, -0.012425201945006847, -0.03367207944393158, -0.013540755026042461, 0.017599312588572502, -0.01685071736574173, -0.006480480544269085, -0.023896312341094017, 0.04106995463371277, 0.02507057972252369, 0.009856495074927807, 0.031294189393520355, 0.007427232339978218, -0.003568667685613036, 0.016146156936883926, -0.017540598288178444, -0.01849468983709812, 0.028402559459209442, 0.03373079001903534, -0.01636633276939392, 0.014634289778769016, -0.007720799185335636, -0.020138662308454514, -0.006829090882092714, -0.012006869539618492, 0.01809837482869625, -0.012241723015904427, 0.003047587350010872, -0.004157635383307934, -0.010935352183878422, -0.02546689473092556, -2.3422249796567485e-05, 0.062412239611148834, 0.00145407160744071, -0.004286070819944143, 0.026142096146941185, 0.009650998748838902, 0.019199248403310776, -0.02418988011777401, -0.00124307069927454, 0.034317925572395325, -0.009100561961531639, -0.021312927827239037, 0.00614654878154397, 0.016630541533231735, -0.012050905264914036, -0.0005522719584405422, 0.02508525736629963, 0.03710680454969406, 0.004040209110826254, -0.027507180348038673, -0.026567768305540085, 0.019933165982365608, 0.007889599539339542, 0.00486219534650445, -0.02549625001847744, -0.009408806450664997, 0.007896939292550087, -0.02153310365974903, 0.005739225074648857, -0.025657711550593376, 0.03584447130560875, 0.03202810510993004, 0.013093066401779652, -0.011133509688079357, -0.011625233106315136, 0.00048484341823495924, -0.03235102817416191, 0.006208931561559439, -0.013291222974658012, 0.011397719383239746, -0.02159181609749794, 0.012535289861261845, -0.011089474894106388, 0.04793940857052803, -0.027727356180548668, 0.02807963639497757, -0.01726171001791954, -0.017878200858831406, 0.023661460727453232, 0.010722516104578972, -0.006491489242762327, 0.02238444611430168, 0.01124359667301178, -0.0018971734680235386, 0.01676264777779579, 0.014098531566560268, 0.016615863889455795, 0.023411927744746208, -0.014722360298037529, 0.0027485163882374763, 0.0006907986826263368, -0.02195877395570278, 0.008249218575656414, 0.01949281617999077, -0.0036163723561912775, -0.05043472349643707, 0.017525920644402504, -0.009005152620375156, -0.029562147334218025, 0.008285914547741413, -0.024865083396434784, -0.01943410187959671, -0.04180387035012245, -0.013511397875845432, 0.006707994733005762, -0.026259522885084152, 0.041216738522052765, -0.011808712966740131, -0.018817612901329994, 0.04133416339755058, -0.0250559002161026, 0.00312831811606884, -0.0140178008005023, 0.03745908662676811, -0.02978232130408287, 0.018215801566839218, -0.024380698800086975, 0.002231105463579297, -0.017393814399838448, 0.026259522885084152, 0.0001342837349511683, -0.025261396542191505, -0.013122422620654106, 0.006007104646414518, 0.006619924679398537, 0.03064834326505661, 0.0038860866334289312, -0.010847282595932484, -0.005133744329214096, 0.0007825382053852081]
    df = pd.DataFrame(data=[[emb]], columns=["EMBD"])
    print(do_embedding_search(df))
    #print(get_table("SEARCH"))
