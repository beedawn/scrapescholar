--
-- PostgreSQL database dump
--

-- Dumped from database version 14.13 (Homebrew)
-- Dumped by pg_dump version 14.13 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: Article; Type: TABLE; Schema: public; Owner: student
--

CREATE TABLE public."Article" (
    article_id integer NOT NULL,
    source_id integer NOT NULL,
    search_id integer NOT NULL,
    user_id integer NOT NULL,
    title character varying NOT NULL,
    citedby integer,
    date date,
    abstract character varying,
    link character varying,
    relevance_score double precision,
    document_type character varying,
    doi character varying
);


ALTER TABLE public."Article" OWNER TO student;

--
-- Name: ArticleScore; Type: TABLE; Schema: public; Owner: student
--

CREATE TABLE public."ArticleScore" (
    article_score_id integer NOT NULL,
    user_id integer NOT NULL,
    article_id integer NOT NULL,
    score double precision NOT NULL,
    last_updated_by_user_id integer,
    evaluation_date timestamp without time zone,
    last_updated_at timestamp without time zone
);


ALTER TABLE public."ArticleScore" OWNER TO student;

--
-- Name: ArticleScore_article_score_id_seq; Type: SEQUENCE; Schema: public; Owner: student
--

CREATE SEQUENCE public."ArticleScore_article_score_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."ArticleScore_article_score_id_seq" OWNER TO student;

--
-- Name: ArticleScore_article_score_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: student
--

ALTER SEQUENCE public."ArticleScore_article_score_id_seq" OWNED BY public."ArticleScore".article_score_id;


--
-- Name: Article_article_id_seq; Type: SEQUENCE; Schema: public; Owner: student
--

CREATE SEQUENCE public."Article_article_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Article_article_id_seq" OWNER TO student;

--
-- Name: Article_article_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: student
--

ALTER SEQUENCE public."Article_article_id_seq" OWNED BY public."Article".article_id;


--
-- Name: Collaboration; Type: TABLE; Schema: public; Owner: student
--

CREATE TABLE public."Collaboration" (
    collaboration_id integer NOT NULL,
    article_id integer,
    user_id integer,
    created_at timestamp without time zone
);


ALTER TABLE public."Collaboration" OWNER TO student;

--
-- Name: Collaboration_collaboration_id_seq; Type: SEQUENCE; Schema: public; Owner: student
--

CREATE SEQUENCE public."Collaboration_collaboration_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Collaboration_collaboration_id_seq" OWNER TO student;

--
-- Name: Collaboration_collaboration_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: student
--

ALTER SEQUENCE public."Collaboration_collaboration_id_seq" OWNED BY public."Collaboration".collaboration_id;


--
-- Name: Comment; Type: TABLE; Schema: public; Owner: student
--

CREATE TABLE public."Comment" (
    comment_id integer NOT NULL,
    article_id integer NOT NULL,
    user_id integer NOT NULL,
    comment_text character varying NOT NULL,
    created_at timestamp without time zone NOT NULL
);


ALTER TABLE public."Comment" OWNER TO student;

--
-- Name: Comment_comment_id_seq; Type: SEQUENCE; Schema: public; Owner: student
--

CREATE SEQUENCE public."Comment_comment_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Comment_comment_id_seq" OWNER TO student;

--
-- Name: Comment_comment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: student
--

ALTER SEQUENCE public."Comment_comment_id_seq" OWNED BY public."Comment".comment_id;


--
-- Name: Keyword; Type: TABLE; Schema: public; Owner: student
--

CREATE TABLE public."Keyword" (
    keyword_id integer NOT NULL,
    keyword character varying(255) NOT NULL
);


ALTER TABLE public."Keyword" OWNER TO student;

--
-- Name: Keyword_keyword_id_seq; Type: SEQUENCE; Schema: public; Owner: student
--

CREATE SEQUENCE public."Keyword_keyword_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Keyword_keyword_id_seq" OWNER TO student;

--
-- Name: Keyword_keyword_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: student
--

ALTER SEQUENCE public."Keyword_keyword_id_seq" OWNED BY public."Keyword".keyword_id;


--
-- Name: ResearchQuestion; Type: TABLE; Schema: public; Owner: student
--

CREATE TABLE public."ResearchQuestion" (
    research_question_id integer NOT NULL,
    research_question text NOT NULL
);


ALTER TABLE public."ResearchQuestion" OWNER TO student;

--
-- Name: ResearchQuestionMapping; Type: TABLE; Schema: public; Owner: student
--

CREATE TABLE public."ResearchQuestionMapping" (
    research_question_mapping_id integer NOT NULL,
    article_id integer,
    research_question_id integer
);


ALTER TABLE public."ResearchQuestionMapping" OWNER TO student;

--
-- Name: ResearchQuestionMapping_research_question_mapping_id_seq; Type: SEQUENCE; Schema: public; Owner: student
--

CREATE SEQUENCE public."ResearchQuestionMapping_research_question_mapping_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."ResearchQuestionMapping_research_question_mapping_id_seq" OWNER TO student;

--
-- Name: ResearchQuestionMapping_research_question_mapping_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: student
--

ALTER SEQUENCE public."ResearchQuestionMapping_research_question_mapping_id_seq" OWNED BY public."ResearchQuestionMapping".research_question_mapping_id;


--
-- Name: ResearchQuestionScore; Type: TABLE; Schema: public; Owner: student
--

CREATE TABLE public."ResearchQuestionScore" (
    research_question_score_id integer NOT NULL,
    research_question_mapping_id integer,
    score integer NOT NULL,
    last_updated_by_id integer
);


ALTER TABLE public."ResearchQuestionScore" OWNER TO student;

--
-- Name: ResearchQuestionScore_research_question_score_id_seq; Type: SEQUENCE; Schema: public; Owner: student
--

CREATE SEQUENCE public."ResearchQuestionScore_research_question_score_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."ResearchQuestionScore_research_question_score_id_seq" OWNER TO student;

--
-- Name: ResearchQuestionScore_research_question_score_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: student
--

ALTER SEQUENCE public."ResearchQuestionScore_research_question_score_id_seq" OWNED BY public."ResearchQuestionScore".research_question_score_id;


--
-- Name: ResearchQuestion_research_question_id_seq; Type: SEQUENCE; Schema: public; Owner: student
--

CREATE SEQUENCE public."ResearchQuestion_research_question_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."ResearchQuestion_research_question_id_seq" OWNER TO student;

--
-- Name: ResearchQuestion_research_question_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: student
--

ALTER SEQUENCE public."ResearchQuestion_research_question_id_seq" OWNED BY public."ResearchQuestion".research_question_id;


--
-- Name: Role; Type: TABLE; Schema: public; Owner: student
--

CREATE TABLE public."Role" (
    role_id integer NOT NULL,
    role_name character varying(50) NOT NULL
);


ALTER TABLE public."Role" OWNER TO student;

--
-- Name: Role_role_id_seq; Type: SEQUENCE; Schema: public; Owner: student
--

CREATE SEQUENCE public."Role_role_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Role_role_id_seq" OWNER TO student;

--
-- Name: Role_role_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: student
--

ALTER SEQUENCE public."Role_role_id_seq" OWNED BY public."Role".role_id;


--
-- Name: Search; Type: TABLE; Schema: public; Owner: student
--

CREATE TABLE public."Search" (
    search_id integer NOT NULL,
    user_id integer,
    search_date timestamp without time zone,
    search_keywords character varying[],
    status character varying(20),
    title character varying(255) NOT NULL
);


ALTER TABLE public."Search" OWNER TO student;

--
-- Name: SearchKeyword; Type: TABLE; Schema: public; Owner: student
--

CREATE TABLE public."SearchKeyword" (
    search_keyword_id integer NOT NULL,
    search_id integer,
    keyword_id integer
);


ALTER TABLE public."SearchKeyword" OWNER TO student;

--
-- Name: SearchKeyword_search_keyword_id_seq; Type: SEQUENCE; Schema: public; Owner: student
--

CREATE SEQUENCE public."SearchKeyword_search_keyword_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."SearchKeyword_search_keyword_id_seq" OWNER TO student;

--
-- Name: SearchKeyword_search_keyword_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: student
--

ALTER SEQUENCE public."SearchKeyword_search_keyword_id_seq" OWNED BY public."SearchKeyword".search_keyword_id;


--
-- Name: SearchShare; Type: TABLE; Schema: public; Owner: student
--

CREATE TABLE public."SearchShare" (
    share_id integer NOT NULL,
    search_id integer,
    shared_with_user_id integer,
    shared_by_user_id integer,
    share_date timestamp without time zone
);


ALTER TABLE public."SearchShare" OWNER TO student;

--
-- Name: SearchShare_share_id_seq; Type: SEQUENCE; Schema: public; Owner: student
--

CREATE SEQUENCE public."SearchShare_share_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."SearchShare_share_id_seq" OWNER TO student;

--
-- Name: SearchShare_share_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: student
--

ALTER SEQUENCE public."SearchShare_share_id_seq" OWNED BY public."SearchShare".share_id;


--
-- Name: Search_search_id_seq; Type: SEQUENCE; Schema: public; Owner: student
--

CREATE SEQUENCE public."Search_search_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Search_search_id_seq" OWNER TO student;

--
-- Name: Search_search_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: student
--

ALTER SEQUENCE public."Search_search_id_seq" OWNED BY public."Search".search_id;


--
-- Name: Source; Type: TABLE; Schema: public; Owner: student
--

CREATE TABLE public."Source" (
    source_id integer NOT NULL,
    name character varying(100) NOT NULL,
    api_endpoint character varying(255),
    scrape_source_url character varying(255)
);


ALTER TABLE public."Source" OWNER TO student;

--
-- Name: Source_source_id_seq; Type: SEQUENCE; Schema: public; Owner: student
--

CREATE SEQUENCE public."Source_source_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Source_source_id_seq" OWNER TO student;

--
-- Name: Source_source_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: student
--

ALTER SEQUENCE public."Source_source_id_seq" OWNED BY public."Source".source_id;


--
-- Name: User; Type: TABLE; Schema: public; Owner: student
--

CREATE TABLE public."User" (
    user_id integer NOT NULL,
    username character varying(255) NOT NULL,
    password character varying(255) NOT NULL,
    role_id integer,
    email character varying(255),
    registration_date timestamp without time zone
);


ALTER TABLE public."User" OWNER TO student;

--
-- Name: UserData; Type: TABLE; Schema: public; Owner: student
--

CREATE TABLE public."UserData" (
    userdata_id integer NOT NULL,
    user_id integer,
    article_id integer,
    relevancy_color character varying(20),
    methodology integer,
    clarity integer,
    transparency integer,
    completeness integer,
    evaluation_criteria character varying
);


ALTER TABLE public."UserData" OWNER TO student;

--
-- Name: UserData_userdata_id_seq; Type: SEQUENCE; Schema: public; Owner: student
--

CREATE SEQUENCE public."UserData_userdata_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."UserData_userdata_id_seq" OWNER TO student;

--
-- Name: UserData_userdata_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: student
--

ALTER SEQUENCE public."UserData_userdata_id_seq" OWNED BY public."UserData".userdata_id;


--
-- Name: User_user_id_seq; Type: SEQUENCE; Schema: public; Owner: student
--

CREATE SEQUENCE public."User_user_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."User_user_id_seq" OWNER TO student;

--
-- Name: User_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: student
--

ALTER SEQUENCE public."User_user_id_seq" OWNED BY public."User".user_id;


--
-- Name: Article article_id; Type: DEFAULT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."Article" ALTER COLUMN article_id SET DEFAULT nextval('public."Article_article_id_seq"'::regclass);


--
-- Name: ArticleScore article_score_id; Type: DEFAULT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."ArticleScore" ALTER COLUMN article_score_id SET DEFAULT nextval('public."ArticleScore_article_score_id_seq"'::regclass);


--
-- Name: Collaboration collaboration_id; Type: DEFAULT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."Collaboration" ALTER COLUMN collaboration_id SET DEFAULT nextval('public."Collaboration_collaboration_id_seq"'::regclass);


--
-- Name: Comment comment_id; Type: DEFAULT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."Comment" ALTER COLUMN comment_id SET DEFAULT nextval('public."Comment_comment_id_seq"'::regclass);


--
-- Name: Keyword keyword_id; Type: DEFAULT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."Keyword" ALTER COLUMN keyword_id SET DEFAULT nextval('public."Keyword_keyword_id_seq"'::regclass);


--
-- Name: ResearchQuestion research_question_id; Type: DEFAULT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."ResearchQuestion" ALTER COLUMN research_question_id SET DEFAULT nextval('public."ResearchQuestion_research_question_id_seq"'::regclass);


--
-- Name: ResearchQuestionMapping research_question_mapping_id; Type: DEFAULT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."ResearchQuestionMapping" ALTER COLUMN research_question_mapping_id SET DEFAULT nextval('public."ResearchQuestionMapping_research_question_mapping_id_seq"'::regclass);


--
-- Name: ResearchQuestionScore research_question_score_id; Type: DEFAULT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."ResearchQuestionScore" ALTER COLUMN research_question_score_id SET DEFAULT nextval('public."ResearchQuestionScore_research_question_score_id_seq"'::regclass);


--
-- Name: Role role_id; Type: DEFAULT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."Role" ALTER COLUMN role_id SET DEFAULT nextval('public."Role_role_id_seq"'::regclass);


--
-- Name: Search search_id; Type: DEFAULT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."Search" ALTER COLUMN search_id SET DEFAULT nextval('public."Search_search_id_seq"'::regclass);


--
-- Name: SearchKeyword search_keyword_id; Type: DEFAULT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."SearchKeyword" ALTER COLUMN search_keyword_id SET DEFAULT nextval('public."SearchKeyword_search_keyword_id_seq"'::regclass);


--
-- Name: SearchShare share_id; Type: DEFAULT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."SearchShare" ALTER COLUMN share_id SET DEFAULT nextval('public."SearchShare_share_id_seq"'::regclass);


--
-- Name: Source source_id; Type: DEFAULT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."Source" ALTER COLUMN source_id SET DEFAULT nextval('public."Source_source_id_seq"'::regclass);


--
-- Name: User user_id; Type: DEFAULT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."User" ALTER COLUMN user_id SET DEFAULT nextval('public."User_user_id_seq"'::regclass);


--
-- Name: UserData userdata_id; Type: DEFAULT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."UserData" ALTER COLUMN userdata_id SET DEFAULT nextval('public."UserData_userdata_id_seq"'::regclass);


--
-- Data for Name: Article; Type: TABLE DATA; Schema: public; Owner: student
--

COPY public."Article" (article_id, source_id, search_id, user_id, title, citedby, date, abstract, link, relevance_score, document_type, doi) FROM stdin;
\.


--
-- Data for Name: ArticleScore; Type: TABLE DATA; Schema: public; Owner: student
--

COPY public."ArticleScore" (article_score_id, user_id, article_id, score, last_updated_by_user_id, evaluation_date, last_updated_at) FROM stdin;
\.


--
-- Data for Name: Collaboration; Type: TABLE DATA; Schema: public; Owner: student
--

COPY public."Collaboration" (collaboration_id, article_id, user_id, created_at) FROM stdin;
\.


--
-- Data for Name: Comment; Type: TABLE DATA; Schema: public; Owner: student
--

COPY public."Comment" (comment_id, article_id, user_id, comment_text, created_at) FROM stdin;
\.


--
-- Data for Name: Keyword; Type: TABLE DATA; Schema: public; Owner: student
--

COPY public."Keyword" (keyword_id, keyword) FROM stdin;
1	example_keyword
2	example_keyword
3	keyword1
4	keyword2
5	keyword3
6	updated_keyword
\.


--
-- Data for Name: ResearchQuestion; Type: TABLE DATA; Schema: public; Owner: student
--

COPY public."ResearchQuestion" (research_question_id, research_question) FROM stdin;
\.


--
-- Data for Name: ResearchQuestionMapping; Type: TABLE DATA; Schema: public; Owner: student
--

COPY public."ResearchQuestionMapping" (research_question_mapping_id, article_id, research_question_id) FROM stdin;
\.


--
-- Data for Name: ResearchQuestionScore; Type: TABLE DATA; Schema: public; Owner: student
--

COPY public."ResearchQuestionScore" (research_question_score_id, research_question_mapping_id, score, last_updated_by_id) FROM stdin;
\.


--
-- Data for Name: Role; Type: TABLE DATA; Schema: public; Owner: student
--

COPY public."Role" (role_id, role_name) FROM stdin;
1	Professor
2	GradStudent
3	Student
4	admin
5	user
6	PHD_Student_20241111071235706252
7	PHD_Student_20241111071235710254
8	User_20241111071235714459
9	Adjunct_Professor_20241111071235714467
10	Project_Manager_20241111071235714470
11	Updated_Role_20241111071235720605
\.


--
-- Data for Name: Search; Type: TABLE DATA; Schema: public; Owner: student
--

COPY public."Search" (search_id, user_id, search_date, search_keywords, status, title) FROM stdin;
1823	1	\N	\N	active	0
1824	1	\N	\N	active	1
1825	1	\N	\N	active	2
1826	1	\N	\N	active	3
1827	1	\N	\N	active	4
1828	1	\N	\N	active	5
1829	1	\N	\N	active	6
1830	1	\N	\N	active	7
1831	1	\N	\N	active	8
1832	1	\N	\N	active	9
1833	1	\N	\N	active	10
1834	1	\N	\N	active	11
1835	1	\N	\N	active	12
1836	1	\N	\N	active	13
1837	1	\N	\N	active	14
1838	1	\N	\N	active	15
1839	1	\N	\N	active	16
1840	1	\N	\N	active	17
1841	1	\N	\N	active	18
1842	1	\N	\N	active	19
1843	1	\N	\N	active	20
1844	1	\N	\N	active	21
1845	1	\N	\N	active	22
1846	1	\N	\N	active	23
1847	1	\N	\N	active	24
1848	1	\N	\N	active	25
1849	1	\N	\N	active	26
1850	1	\N	\N	active	27
1851	1	\N	\N	active	28
1852	1	\N	\N	active	29
1853	1	\N	\N	active	30
1854	1	\N	\N	active	31
1855	1	\N	\N	active	32
1856	1	\N	\N	active	33
1857	1	\N	\N	active	34
1858	1	\N	\N	active	35
1859	1	\N	\N	active	36
1860	1	\N	\N	active	37
1861	1	\N	\N	active	38
1862	1	\N	\N	active	39
1863	1	\N	\N	active	40
1864	1	\N	\N	active	41
1865	1	\N	\N	active	42
1866	1	\N	\N	active	43
1867	1	\N	\N	active	44
1868	1	\N	\N	active	45
1869	1	\N	\N	active	46
1870	1	\N	\N	active	47
1871	1	\N	\N	active	48
1872	1	\N	\N	active	49
1873	1	\N	\N	active	50
1874	1	\N	\N	active	51
1875	1	\N	\N	active	52
1876	1	\N	\N	active	53
1877	1	\N	\N	active	54
1878	1	\N	\N	active	55
1879	1	\N	\N	active	56
1880	1	\N	\N	active	57
1881	1	\N	\N	active	58
1882	1	\N	\N	active	59
1883	1	\N	\N	active	60
1884	1	\N	\N	active	61
1885	1	\N	\N	active	62
1886	1	\N	\N	active	63
1887	1	\N	\N	active	64
1888	1	\N	\N	active	65
1889	1	\N	\N	active	66
1890	1	\N	\N	active	67
1891	1	\N	\N	active	68
1892	1	\N	\N	active	69
1893	1	\N	\N	active	70
1894	1	\N	\N	active	71
1895	1	\N	\N	active	72
1896	1	\N	\N	active	73
1897	1	\N	\N	active	74
1898	1	\N	\N	active	75
1899	1	\N	\N	active	76
1900	1	\N	\N	active	77
1901	1	\N	\N	active	78
1902	1	\N	\N	active	79
1903	1	\N	\N	active	80
1904	1	\N	\N	active	81
1905	1	\N	\N	active	82
1906	1	\N	\N	active	83
1907	1	\N	\N	active	84
1908	1	\N	\N	active	85
1909	1	\N	\N	active	86
1910	1	\N	\N	active	87
1911	1	\N	\N	active	88
1912	1	\N	\N	active	89
1913	1	\N	\N	active	90
1914	1	\N	\N	active	91
1915	1	\N	\N	active	92
1916	1	\N	\N	active	93
1917	1	\N	\N	active	94
1918	1	\N	\N	active	95
1919	1	\N	\N	active	96
1920	1	\N	\N	active	97
1921	1	\N	\N	active	98
1922	1	\N	\N	active	99
1923	1	\N	\N	active	100
1924	1	\N	\N	active	101
1925	1	\N	\N	active	102
1926	1	\N	\N	active	103
1927	1	\N	\N	active	104
1928	1	\N	\N	active	105
1929	1	\N	\N	active	106
1930	1	\N	\N	active	107
1931	1	\N	\N	active	108
1932	1	\N	\N	active	109
1933	1	\N	\N	active	110
1934	1	\N	\N	active	111
1935	1	\N	\N	active	112
1936	1	\N	\N	active	113
1937	1	\N	\N	active	114
1938	1	\N	\N	active	115
1939	1	\N	\N	active	116
1940	1	\N	\N	active	117
1941	1	\N	\N	active	118
1942	1	\N	\N	active	119
1943	1	\N	\N	active	120
1944	1	\N	\N	active	121
1945	1	\N	\N	active	122
1946	1	\N	\N	active	123
1947	1	\N	\N	active	124
1948	1	\N	\N	active	125
1949	1	\N	\N	active	126
1950	1	\N	\N	active	127
1951	1	\N	\N	active	128
1952	1	\N	\N	active	129
1953	1	\N	\N	active	130
1954	1	\N	\N	active	131
1955	1	\N	\N	active	132
1956	1	\N	\N	active	133
1957	1	\N	\N	active	134
1958	1	\N	\N	active	135
1959	1	\N	\N	active	136
1960	1	\N	\N	active	137
1961	1	\N	\N	active	138
1962	1	\N	\N	active	139
1963	1	\N	\N	active	140
1964	1	\N	\N	active	141
1965	1	\N	\N	active	142
1966	1	\N	\N	active	143
1967	1	\N	\N	active	144
1968	1	\N	\N	active	145
1969	1	\N	\N	active	146
1970	1	\N	\N	active	147
1971	1	\N	\N	active	148
1972	1	\N	\N	active	149
1973	1	\N	\N	active	150
1974	1	\N	\N	active	151
1975	1	\N	\N	active	152
1976	1	\N	\N	active	153
1977	1	\N	\N	active	154
1978	1	\N	\N	active	155
1979	1	\N	\N	active	156
1980	1	\N	\N	active	157
1981	1	\N	\N	active	158
1982	1	\N	\N	active	159
1983	1	\N	\N	active	160
1984	1	\N	\N	active	161
1985	1	\N	\N	active	162
1986	1	\N	\N	active	163
1987	1	\N	\N	active	164
1988	1	\N	\N	active	165
1989	1	\N	\N	active	166
1990	1	\N	\N	active	167
1991	1	\N	\N	active	168
1992	1	\N	\N	active	169
1993	1	\N	\N	active	170
1994	1	\N	\N	active	171
1995	1	\N	\N	active	172
1996	1	\N	\N	active	173
1997	1	\N	\N	active	174
1998	1	\N	\N	active	175
1999	1	\N	\N	active	176
2000	1	\N	\N	active	177
2001	1	\N	\N	active	178
2002	1	\N	\N	active	179
2003	1	\N	\N	active	180
2004	1	\N	\N	active	181
2005	1	\N	\N	active	182
2006	1	\N	\N	active	183
2007	1	\N	\N	active	184
2008	1	\N	\N	active	185
2009	1	\N	\N	active	186
2010	1	\N	\N	active	187
2011	1	\N	\N	active	188
2012	1	\N	\N	active	189
2013	1	\N	\N	active	190
2014	1	\N	\N	active	191
2015	1	\N	\N	active	192
2016	1	\N	\N	active	193
2017	1	\N	\N	active	194
2018	1	\N	\N	active	195
2019	1	\N	\N	active	196
2020	1	\N	\N	active	197
2021	1	\N	\N	active	198
2022	1	\N	\N	active	199
2023	1	\N	\N	active	200
2024	1	\N	\N	active	201
2025	1	\N	\N	active	202
2026	1	\N	\N	active	203
2027	1	\N	\N	active	204
2028	1	\N	\N	active	205
2029	1	\N	\N	active	206
2030	1	\N	\N	active	207
2031	1	\N	\N	active	208
2032	1	\N	\N	active	209
2033	1	\N	\N	active	210
2034	1	\N	\N	active	211
2035	1	\N	\N	active	212
2036	1	\N	\N	active	213
2037	1	\N	\N	active	214
2038	1	\N	\N	active	215
2039	1	\N	\N	active	216
2040	1	\N	\N	active	217
2041	1	\N	\N	active	218
2042	1	\N	\N	active	219
2043	1	\N	\N	active	220
2044	1	\N	\N	active	221
2045	1	\N	\N	active	222
2046	1	\N	\N	active	223
2047	1	\N	\N	active	224
2048	1	\N	\N	active	225
2049	1	\N	\N	active	226
2050	1	\N	\N	active	227
2051	1	\N	\N	active	228
2052	1	\N	\N	active	229
2053	1	\N	\N	active	230
2054	1	\N	\N	active	231
2055	1	\N	\N	active	232
2056	1	\N	\N	active	233
2057	1	\N	\N	active	234
2058	1	\N	\N	active	235
2059	1	\N	\N	active	236
2060	1	\N	\N	active	237
2061	1	\N	\N	active	238
2062	1	\N	\N	active	239
2063	1	\N	\N	active	240
2064	1	\N	\N	active	241
2065	1	\N	\N	active	242
2066	1	\N	\N	active	243
2067	1	\N	\N	active	244
2068	1	\N	\N	active	245
2069	1	\N	\N	active	246
2070	1	\N	\N	active	247
2071	1	\N	\N	active	248
2072	1	\N	\N	active	249
2073	1	\N	\N	active	250
2074	1	\N	\N	active	251
2075	1	\N	\N	active	252
2076	1	\N	\N	active	253
2077	1	\N	\N	active	254
2078	1	\N	\N	active	255
2079	1	\N	\N	active	256
2080	1	\N	\N	active	257
2081	1	\N	\N	active	258
2082	1	\N	\N	active	259
2083	1	\N	\N	active	260
2084	1	\N	\N	active	261
2085	1	\N	\N	active	262
2086	1	\N	\N	active	263
2087	1	\N	\N	active	264
2088	1	\N	\N	active	265
2089	1	\N	\N	active	266
2090	1	\N	\N	active	267
2091	1	\N	\N	active	268
2092	1	\N	\N	active	269
2093	1	\N	\N	active	270
2094	1	\N	\N	active	271
2095	1	\N	\N	active	272
2096	1	\N	\N	active	273
2097	1	\N	\N	active	274
2098	1	\N	\N	active	275
2099	1	\N	\N	active	276
2100	1	\N	\N	active	277
2101	1	\N	\N	active	278
2102	1	\N	\N	active	279
2103	1	\N	\N	active	280
2104	1	\N	\N	active	281
2105	1	\N	\N	active	282
2106	1	\N	\N	active	283
2107	1	\N	\N	active	284
2108	1	\N	\N	active	285
2109	1	\N	\N	active	286
2110	1	\N	\N	active	287
2111	1	\N	\N	active	288
2112	1	\N	\N	active	289
2113	1	\N	\N	active	290
2114	1	\N	\N	active	291
2115	1	\N	\N	active	292
2116	1	\N	\N	active	293
2117	1	\N	\N	active	294
2118	1	\N	\N	active	295
2119	1	\N	\N	active	296
2120	1	\N	\N	active	297
2121	1	\N	\N	active	298
2122	1	\N	\N	active	299
2123	1	\N	\N	active	300
3189	1	\N	\N	active	162
3190	1	\N	\N	active	163
3191	1	\N	\N	active	164
3192	1	\N	\N	active	165
3193	1	\N	\N	active	166
3194	1	\N	\N	active	167
3195	1	\N	\N	active	168
3196	1	\N	\N	active	169
3197	1	\N	\N	active	170
3198	1	\N	\N	active	171
3199	1	\N	\N	active	172
3200	1	\N	\N	active	173
3201	1	\N	\N	active	174
2124	1	\N	\N	active	0
2125	1	\N	\N	active	1
2126	1	\N	\N	active	2
2127	1	\N	\N	active	3
2128	1	\N	\N	active	4
2129	1	\N	\N	active	5
2130	1	\N	\N	active	6
2131	1	\N	\N	active	7
2132	1	\N	\N	active	8
2133	1	\N	\N	active	9
2134	1	\N	\N	active	10
2135	1	\N	\N	active	11
2136	1	\N	\N	active	12
2137	1	\N	\N	active	13
2138	1	\N	\N	active	14
2139	1	\N	\N	active	15
2140	1	\N	\N	active	16
2141	1	\N	\N	active	17
2142	1	\N	\N	active	18
2143	1	\N	\N	active	19
2144	1	\N	\N	active	20
2145	1	\N	\N	active	21
2146	1	\N	\N	active	22
2147	1	\N	\N	active	23
2148	1	\N	\N	active	24
2149	1	\N	\N	active	25
2150	1	\N	\N	active	26
2151	1	\N	\N	active	27
2152	1	\N	\N	active	28
2153	1	\N	\N	active	29
2154	1	\N	\N	active	30
2155	1	\N	\N	active	31
2156	1	\N	\N	active	32
2157	1	\N	\N	active	33
2158	1	\N	\N	active	34
2159	1	\N	\N	active	35
2160	1	\N	\N	active	36
2161	1	\N	\N	active	37
2162	1	\N	\N	active	38
2163	1	\N	\N	active	39
2164	1	\N	\N	active	40
2165	1	\N	\N	active	41
2166	1	\N	\N	active	42
2167	1	\N	\N	active	43
2168	1	\N	\N	active	44
2169	1	\N	\N	active	45
2170	1	\N	\N	active	46
2171	1	\N	\N	active	47
2172	1	\N	\N	active	48
2173	1	\N	\N	active	49
2174	1	\N	\N	active	50
2175	1	\N	\N	active	51
2176	1	\N	\N	active	52
2177	1	\N	\N	active	53
2178	1	\N	\N	active	54
2179	1	\N	\N	active	55
2180	1	\N	\N	active	56
2181	1	\N	\N	active	57
2182	1	\N	\N	active	58
2183	1	\N	\N	active	59
2184	1	\N	\N	active	60
2185	1	\N	\N	active	61
2186	1	\N	\N	active	62
2187	1	\N	\N	active	63
2188	1	\N	\N	active	64
2189	1	\N	\N	active	65
2190	1	\N	\N	active	66
2191	1	\N	\N	active	67
2192	1	\N	\N	active	68
2193	1	\N	\N	active	69
2194	1	\N	\N	active	70
2195	1	\N	\N	active	71
2196	1	\N	\N	active	72
2197	1	\N	\N	active	73
2198	1	\N	\N	active	74
2199	1	\N	\N	active	75
2200	1	\N	\N	active	76
2201	1	\N	\N	active	77
2202	1	\N	\N	active	78
2203	1	\N	\N	active	79
2204	1	\N	\N	active	80
2205	1	\N	\N	active	81
2206	1	\N	\N	active	82
2207	1	\N	\N	active	83
2208	1	\N	\N	active	84
2209	1	\N	\N	active	85
2210	1	\N	\N	active	86
2211	1	\N	\N	active	87
2212	1	\N	\N	active	88
2213	1	\N	\N	active	89
2214	1	\N	\N	active	90
2215	1	\N	\N	active	91
2216	1	\N	\N	active	92
2217	1	\N	\N	active	93
2218	1	\N	\N	active	94
2219	1	\N	\N	active	95
2220	1	\N	\N	active	96
2221	1	\N	\N	active	97
2222	1	\N	\N	active	98
2223	1	\N	\N	active	99
2224	1	\N	\N	active	100
2225	1	\N	\N	active	101
2226	1	\N	\N	active	102
2227	1	\N	\N	active	103
2228	1	\N	\N	active	104
2229	1	\N	\N	active	105
2230	1	\N	\N	active	106
2231	1	\N	\N	active	107
2232	1	\N	\N	active	108
2233	1	\N	\N	active	109
2234	1	\N	\N	active	110
2235	1	\N	\N	active	111
2236	1	\N	\N	active	112
2237	1	\N	\N	active	113
2238	1	\N	\N	active	114
2239	1	\N	\N	active	115
2240	1	\N	\N	active	116
2241	1	\N	\N	active	117
2242	1	\N	\N	active	118
2243	1	\N	\N	active	119
2244	1	\N	\N	active	120
2245	1	\N	\N	active	121
2246	1	\N	\N	active	122
2247	1	\N	\N	active	123
2248	1	\N	\N	active	124
2249	1	\N	\N	active	125
2250	1	\N	\N	active	126
2251	1	\N	\N	active	127
2252	1	\N	\N	active	128
2253	1	\N	\N	active	129
2254	1	\N	\N	active	130
2255	1	\N	\N	active	131
2256	1	\N	\N	active	132
2257	1	\N	\N	active	133
2258	1	\N	\N	active	134
2259	1	\N	\N	active	135
2260	1	\N	\N	active	136
2261	1	\N	\N	active	137
2262	1	\N	\N	active	138
2263	1	\N	\N	active	139
2264	1	\N	\N	active	140
2265	1	\N	\N	active	141
2266	1	\N	\N	active	142
2267	1	\N	\N	active	143
2268	1	\N	\N	active	144
2269	1	\N	\N	active	145
2270	1	\N	\N	active	146
2271	1	\N	\N	active	147
2272	1	\N	\N	active	148
2273	1	\N	\N	active	149
2274	1	\N	\N	active	150
2275	1	\N	\N	active	151
2276	1	\N	\N	active	152
2277	1	\N	\N	active	153
2278	1	\N	\N	active	154
2279	1	\N	\N	active	155
2280	1	\N	\N	active	156
2281	1	\N	\N	active	157
2282	1	\N	\N	active	158
2283	1	\N	\N	active	159
2284	1	\N	\N	active	160
2285	1	\N	\N	active	161
2286	1	\N	\N	active	162
2287	1	\N	\N	active	163
2288	1	\N	\N	active	164
2289	1	\N	\N	active	165
2290	1	\N	\N	active	166
2291	1	\N	\N	active	167
2292	1	\N	\N	active	168
2293	1	\N	\N	active	169
2294	1	\N	\N	active	170
2295	1	\N	\N	active	171
2296	1	\N	\N	active	172
2297	1	\N	\N	active	173
2298	1	\N	\N	active	174
2299	1	\N	\N	active	175
2300	1	\N	\N	active	176
2301	1	\N	\N	active	177
2302	1	\N	\N	active	178
2303	1	\N	\N	active	179
2304	1	\N	\N	active	180
2305	1	\N	\N	active	181
2306	1	\N	\N	active	182
2307	1	\N	\N	active	183
2308	1	\N	\N	active	184
2309	1	\N	\N	active	185
2310	1	\N	\N	active	186
2311	1	\N	\N	active	187
2312	1	\N	\N	active	188
2313	1	\N	\N	active	189
2314	1	\N	\N	active	190
2315	1	\N	\N	active	191
2316	1	\N	\N	active	192
2317	1	\N	\N	active	193
2318	1	\N	\N	active	194
2319	1	\N	\N	active	195
2320	1	\N	\N	active	196
2321	1	\N	\N	active	197
2322	1	\N	\N	active	198
2323	1	\N	\N	active	199
2324	1	\N	\N	active	200
2325	1	\N	\N	active	201
2326	1	\N	\N	active	202
2327	1	\N	\N	active	203
2328	1	\N	\N	active	204
2329	1	\N	\N	active	205
2330	1	\N	\N	active	206
2331	1	\N	\N	active	207
2332	1	\N	\N	active	208
2333	1	\N	\N	active	209
2334	1	\N	\N	active	210
2335	1	\N	\N	active	211
2336	1	\N	\N	active	212
2337	1	\N	\N	active	213
2338	1	\N	\N	active	214
2339	1	\N	\N	active	215
2340	1	\N	\N	active	216
2341	1	\N	\N	active	217
2342	1	\N	\N	active	218
2343	1	\N	\N	active	219
2344	1	\N	\N	active	220
2345	1	\N	\N	active	221
2346	1	\N	\N	active	222
2347	1	\N	\N	active	223
2348	1	\N	\N	active	224
2349	1	\N	\N	active	225
2350	1	\N	\N	active	226
2351	1	\N	\N	active	227
2352	1	\N	\N	active	228
2353	1	\N	\N	active	229
2354	1	\N	\N	active	230
2355	1	\N	\N	active	231
2356	1	\N	\N	active	232
2357	1	\N	\N	active	233
2358	1	\N	\N	active	234
2359	1	\N	\N	active	235
2360	1	\N	\N	active	236
2361	1	\N	\N	active	237
2362	1	\N	\N	active	238
2363	1	\N	\N	active	239
2364	1	\N	\N	active	240
2365	1	\N	\N	active	241
2366	1	\N	\N	active	242
2367	1	\N	\N	active	243
2368	1	\N	\N	active	244
2369	1	\N	\N	active	245
2370	1	\N	\N	active	246
2371	1	\N	\N	active	247
2372	1	\N	\N	active	248
2373	1	\N	\N	active	249
2374	1	\N	\N	active	250
2375	1	\N	\N	active	251
2376	1	\N	\N	active	252
2377	1	\N	\N	active	253
2378	1	\N	\N	active	254
2379	1	\N	\N	active	255
2380	1	\N	\N	active	256
2381	1	\N	\N	active	257
2382	1	\N	\N	active	258
2383	1	\N	\N	active	259
2384	1	\N	\N	active	260
2385	1	\N	\N	active	261
2386	1	\N	\N	active	262
2387	1	\N	\N	active	263
2388	1	\N	\N	active	264
2389	1	\N	\N	active	265
2390	1	\N	\N	active	266
2391	1	\N	\N	active	267
2392	1	\N	\N	active	268
2393	1	\N	\N	active	269
2394	1	\N	\N	active	270
2395	1	\N	\N	active	271
2396	1	\N	\N	active	272
2397	1	\N	\N	active	273
2398	1	\N	\N	active	274
2399	1	\N	\N	active	275
2400	1	\N	\N	active	276
2401	1	\N	\N	active	277
2402	1	\N	\N	active	278
2403	1	\N	\N	active	279
2404	1	\N	\N	active	280
2405	1	\N	\N	active	281
2406	1	\N	\N	active	282
2407	1	\N	\N	active	283
2408	1	\N	\N	active	284
2409	1	\N	\N	active	285
2410	1	\N	\N	active	286
2411	1	\N	\N	active	287
2412	1	\N	\N	active	288
2413	1	\N	\N	active	289
2414	1	\N	\N	active	290
2415	1	\N	\N	active	291
2416	1	\N	\N	active	292
2417	1	\N	\N	active	293
2418	1	\N	\N	active	294
2419	1	\N	\N	active	295
2420	1	\N	\N	active	296
2421	1	\N	\N	active	297
2422	1	\N	\N	active	298
2423	1	\N	\N	active	299
2424	1	\N	\N	active	300
3202	1	\N	\N	active	175
3203	1	\N	\N	active	176
3204	1	\N	\N	active	177
3205	1	\N	\N	active	178
3206	1	\N	\N	active	179
3207	1	\N	\N	active	180
3208	1	\N	\N	active	181
3209	1	\N	\N	active	182
3210	1	\N	\N	active	183
3211	1	\N	\N	active	184
3212	1	\N	\N	active	185
3213	1	\N	\N	active	186
3214	1	\N	\N	active	187
2425	1	\N	\N	active	0
2426	1	\N	\N	active	1
2427	1	\N	\N	active	2
2428	1	\N	\N	active	3
2429	1	\N	\N	active	4
2430	1	\N	\N	active	5
2431	1	\N	\N	active	6
2432	1	\N	\N	active	7
2433	1	\N	\N	active	8
2434	1	\N	\N	active	9
2435	1	\N	\N	active	10
2436	1	\N	\N	active	11
2437	1	\N	\N	active	12
2438	1	\N	\N	active	13
2439	1	\N	\N	active	14
2440	1	\N	\N	active	15
2441	1	\N	\N	active	16
2442	1	\N	\N	active	17
2443	1	\N	\N	active	18
2444	1	\N	\N	active	19
2445	1	\N	\N	active	20
2446	1	\N	\N	active	21
2447	1	\N	\N	active	22
2448	1	\N	\N	active	23
2449	1	\N	\N	active	24
2450	1	\N	\N	active	25
2451	1	\N	\N	active	26
2452	1	\N	\N	active	27
2453	1	\N	\N	active	28
2454	1	\N	\N	active	29
2455	1	\N	\N	active	30
2456	1	\N	\N	active	31
2457	1	\N	\N	active	32
2458	1	\N	\N	active	33
2459	1	\N	\N	active	34
2460	1	\N	\N	active	35
2461	1	\N	\N	active	36
2462	1	\N	\N	active	37
2463	1	\N	\N	active	38
2464	1	\N	\N	active	39
2465	1	\N	\N	active	40
2466	1	\N	\N	active	41
2467	1	\N	\N	active	42
2468	1	\N	\N	active	43
2469	1	\N	\N	active	44
2470	1	\N	\N	active	45
2471	1	\N	\N	active	46
2472	1	\N	\N	active	47
2473	1	\N	\N	active	48
2474	1	\N	\N	active	49
2475	1	\N	\N	active	50
2476	1	\N	\N	active	51
2477	1	\N	\N	active	52
2478	1	\N	\N	active	53
2479	1	\N	\N	active	54
2480	1	\N	\N	active	55
2481	1	\N	\N	active	56
2482	1	\N	\N	active	57
2483	1	\N	\N	active	58
2484	1	\N	\N	active	59
2485	1	\N	\N	active	60
2486	1	\N	\N	active	61
2487	1	\N	\N	active	62
2488	1	\N	\N	active	63
2489	1	\N	\N	active	64
2490	1	\N	\N	active	65
2491	1	\N	\N	active	66
2492	1	\N	\N	active	67
2493	1	\N	\N	active	68
2494	1	\N	\N	active	69
2495	1	\N	\N	active	70
2496	1	\N	\N	active	71
2497	1	\N	\N	active	72
2498	1	\N	\N	active	73
2499	1	\N	\N	active	74
2500	1	\N	\N	active	75
2501	1	\N	\N	active	76
2502	1	\N	\N	active	77
2503	1	\N	\N	active	78
2504	1	\N	\N	active	79
2505	1	\N	\N	active	80
2506	1	\N	\N	active	81
2507	1	\N	\N	active	82
2508	1	\N	\N	active	83
2509	1	\N	\N	active	84
2510	1	\N	\N	active	85
2511	1	\N	\N	active	86
2512	1	\N	\N	active	87
2513	1	\N	\N	active	88
2514	1	\N	\N	active	89
2515	1	\N	\N	active	90
2516	1	\N	\N	active	91
2517	1	\N	\N	active	92
2518	1	\N	\N	active	93
2519	1	\N	\N	active	94
2520	1	\N	\N	active	95
2521	1	\N	\N	active	96
2522	1	\N	\N	active	97
2523	1	\N	\N	active	98
2524	1	\N	\N	active	99
2525	1	\N	\N	active	100
2526	1	\N	\N	active	101
2527	1	\N	\N	active	102
2528	1	\N	\N	active	103
2529	1	\N	\N	active	104
2530	1	\N	\N	active	105
2531	1	\N	\N	active	106
2532	1	\N	\N	active	107
2533	1	\N	\N	active	108
2534	1	\N	\N	active	109
2535	1	\N	\N	active	110
2536	1	\N	\N	active	111
2537	1	\N	\N	active	112
2538	1	\N	\N	active	113
2539	1	\N	\N	active	114
2540	1	\N	\N	active	115
2541	1	\N	\N	active	116
2542	1	\N	\N	active	117
2543	1	\N	\N	active	118
2544	1	\N	\N	active	119
2545	1	\N	\N	active	120
2546	1	\N	\N	active	121
2547	1	\N	\N	active	122
2548	1	\N	\N	active	123
2549	1	\N	\N	active	124
2550	1	\N	\N	active	125
2551	1	\N	\N	active	126
2552	1	\N	\N	active	127
2553	1	\N	\N	active	128
2554	1	\N	\N	active	129
2555	1	\N	\N	active	130
2556	1	\N	\N	active	131
2557	1	\N	\N	active	132
2558	1	\N	\N	active	133
2559	1	\N	\N	active	134
2560	1	\N	\N	active	135
2561	1	\N	\N	active	136
2562	1	\N	\N	active	137
2563	1	\N	\N	active	138
2564	1	\N	\N	active	139
2565	1	\N	\N	active	140
2566	1	\N	\N	active	141
2567	1	\N	\N	active	142
2568	1	\N	\N	active	143
2569	1	\N	\N	active	144
2570	1	\N	\N	active	145
2571	1	\N	\N	active	146
2572	1	\N	\N	active	147
2573	1	\N	\N	active	148
2574	1	\N	\N	active	149
2575	1	\N	\N	active	150
2576	1	\N	\N	active	151
2577	1	\N	\N	active	152
2578	1	\N	\N	active	153
2579	1	\N	\N	active	154
2580	1	\N	\N	active	155
2581	1	\N	\N	active	156
2582	1	\N	\N	active	157
2583	1	\N	\N	active	158
2584	1	\N	\N	active	159
2585	1	\N	\N	active	160
2586	1	\N	\N	active	161
2587	1	\N	\N	active	162
2588	1	\N	\N	active	163
2589	1	\N	\N	active	164
2590	1	\N	\N	active	165
2591	1	\N	\N	active	166
2592	1	\N	\N	active	167
2593	1	\N	\N	active	168
2594	1	\N	\N	active	169
2595	1	\N	\N	active	170
2596	1	\N	\N	active	171
2597	1	\N	\N	active	172
2598	1	\N	\N	active	173
2599	1	\N	\N	active	174
2600	1	\N	\N	active	175
2601	1	\N	\N	active	176
2602	1	\N	\N	active	177
2603	1	\N	\N	active	178
2604	1	\N	\N	active	179
2605	1	\N	\N	active	180
2606	1	\N	\N	active	181
2607	1	\N	\N	active	182
2608	1	\N	\N	active	183
2609	1	\N	\N	active	184
2610	1	\N	\N	active	185
2611	1	\N	\N	active	186
2612	1	\N	\N	active	187
2613	1	\N	\N	active	188
2614	1	\N	\N	active	189
2615	1	\N	\N	active	190
2616	1	\N	\N	active	191
2617	1	\N	\N	active	192
2618	1	\N	\N	active	193
2619	1	\N	\N	active	194
2620	1	\N	\N	active	195
2621	1	\N	\N	active	196
2622	1	\N	\N	active	197
2623	1	\N	\N	active	198
2624	1	\N	\N	active	199
2625	1	\N	\N	active	200
2626	1	\N	\N	active	201
2627	1	\N	\N	active	202
2628	1	\N	\N	active	203
2629	1	\N	\N	active	204
2630	1	\N	\N	active	205
2631	1	\N	\N	active	206
2632	1	\N	\N	active	207
2633	1	\N	\N	active	208
2634	1	\N	\N	active	209
2635	1	\N	\N	active	210
2636	1	\N	\N	active	211
2637	1	\N	\N	active	212
2638	1	\N	\N	active	213
2639	1	\N	\N	active	214
2640	1	\N	\N	active	215
2641	1	\N	\N	active	216
2642	1	\N	\N	active	217
2643	1	\N	\N	active	218
2644	1	\N	\N	active	219
2645	1	\N	\N	active	220
2646	1	\N	\N	active	221
2647	1	\N	\N	active	222
2648	1	\N	\N	active	223
2649	1	\N	\N	active	224
2650	1	\N	\N	active	225
2651	1	\N	\N	active	226
2652	1	\N	\N	active	227
2653	1	\N	\N	active	228
2654	1	\N	\N	active	229
2655	1	\N	\N	active	230
2656	1	\N	\N	active	231
2657	1	\N	\N	active	232
2658	1	\N	\N	active	233
2659	1	\N	\N	active	234
2660	1	\N	\N	active	235
2661	1	\N	\N	active	236
2662	1	\N	\N	active	237
2663	1	\N	\N	active	238
2664	1	\N	\N	active	239
2665	1	\N	\N	active	240
2666	1	\N	\N	active	241
2667	1	\N	\N	active	242
2668	1	\N	\N	active	243
2669	1	\N	\N	active	244
2670	1	\N	\N	active	245
2671	1	\N	\N	active	246
2672	1	\N	\N	active	247
2673	1	\N	\N	active	248
2674	1	\N	\N	active	249
2675	1	\N	\N	active	250
2676	1	\N	\N	active	251
2677	1	\N	\N	active	252
2678	1	\N	\N	active	253
2679	1	\N	\N	active	254
2680	1	\N	\N	active	255
2681	1	\N	\N	active	256
2682	1	\N	\N	active	257
2683	1	\N	\N	active	258
2684	1	\N	\N	active	259
2685	1	\N	\N	active	260
2686	1	\N	\N	active	261
2687	1	\N	\N	active	262
2688	1	\N	\N	active	263
2689	1	\N	\N	active	264
2690	1	\N	\N	active	265
2691	1	\N	\N	active	266
2692	1	\N	\N	active	267
2693	1	\N	\N	active	268
2694	1	\N	\N	active	269
2695	1	\N	\N	active	270
2696	1	\N	\N	active	271
2697	1	\N	\N	active	272
2698	1	\N	\N	active	273
2699	1	\N	\N	active	274
2700	1	\N	\N	active	275
2701	1	\N	\N	active	276
2702	1	\N	\N	active	277
2703	1	\N	\N	active	278
2704	1	\N	\N	active	279
2705	1	\N	\N	active	280
2706	1	\N	\N	active	281
2707	1	\N	\N	active	282
2708	1	\N	\N	active	283
2709	1	\N	\N	active	284
2710	1	\N	\N	active	285
2711	1	\N	\N	active	286
2712	1	\N	\N	active	287
2713	1	\N	\N	active	288
2714	1	\N	\N	active	289
2715	1	\N	\N	active	290
2716	1	\N	\N	active	291
2717	1	\N	\N	active	292
2718	1	\N	\N	active	293
2719	1	\N	\N	active	294
2720	1	\N	\N	active	295
2721	1	\N	\N	active	296
2722	1	\N	\N	active	297
2723	1	\N	\N	active	298
2724	1	\N	\N	active	299
2725	1	\N	\N	active	300
3215	1	\N	\N	active	188
3216	1	\N	\N	active	189
3217	1	\N	\N	active	190
3218	1	\N	\N	active	191
3219	1	\N	\N	active	192
3220	1	\N	\N	active	193
3221	1	\N	\N	active	194
3222	1	\N	\N	active	195
3223	1	\N	\N	active	196
3224	1	\N	\N	active	197
3225	1	\N	\N	active	198
3226	1	\N	\N	active	199
3227	1	\N	\N	active	200
2726	1	\N	\N	active	0
2727	1	\N	\N	active	1
2728	1	\N	\N	active	2
2729	1	\N	\N	active	3
2730	1	\N	\N	active	4
2731	1	\N	\N	active	5
2732	1	\N	\N	active	6
2733	1	\N	\N	active	7
2734	1	\N	\N	active	8
2735	1	\N	\N	active	9
2736	1	\N	\N	active	10
2737	1	\N	\N	active	11
2738	1	\N	\N	active	12
2739	1	\N	\N	active	13
2740	1	\N	\N	active	14
2741	1	\N	\N	active	15
2742	1	\N	\N	active	16
2743	1	\N	\N	active	17
2744	1	\N	\N	active	18
2745	1	\N	\N	active	19
2746	1	\N	\N	active	20
2747	1	\N	\N	active	21
2748	1	\N	\N	active	22
2749	1	\N	\N	active	23
2750	1	\N	\N	active	24
2751	1	\N	\N	active	25
2752	1	\N	\N	active	26
2753	1	\N	\N	active	27
2754	1	\N	\N	active	28
2755	1	\N	\N	active	29
2756	1	\N	\N	active	30
2757	1	\N	\N	active	31
2758	1	\N	\N	active	32
2759	1	\N	\N	active	33
2760	1	\N	\N	active	34
2761	1	\N	\N	active	35
2762	1	\N	\N	active	36
2763	1	\N	\N	active	37
2764	1	\N	\N	active	38
2765	1	\N	\N	active	39
2766	1	\N	\N	active	40
2767	1	\N	\N	active	41
2768	1	\N	\N	active	42
2769	1	\N	\N	active	43
2770	1	\N	\N	active	44
2771	1	\N	\N	active	45
2772	1	\N	\N	active	46
2773	1	\N	\N	active	47
2774	1	\N	\N	active	48
2775	1	\N	\N	active	49
2776	1	\N	\N	active	50
2777	1	\N	\N	active	51
2778	1	\N	\N	active	52
2779	1	\N	\N	active	53
2780	1	\N	\N	active	54
2781	1	\N	\N	active	55
2782	1	\N	\N	active	56
2783	1	\N	\N	active	57
2784	1	\N	\N	active	58
2785	1	\N	\N	active	59
2786	1	\N	\N	active	60
2787	1	\N	\N	active	61
2788	1	\N	\N	active	62
2789	1	\N	\N	active	63
2790	1	\N	\N	active	64
2791	1	\N	\N	active	65
2792	1	\N	\N	active	66
2793	1	\N	\N	active	67
2794	1	\N	\N	active	68
2795	1	\N	\N	active	69
2796	1	\N	\N	active	70
2797	1	\N	\N	active	71
2798	1	\N	\N	active	72
2799	1	\N	\N	active	73
2800	1	\N	\N	active	74
2801	1	\N	\N	active	75
2802	1	\N	\N	active	76
2803	1	\N	\N	active	77
2804	1	\N	\N	active	78
2805	1	\N	\N	active	79
2806	1	\N	\N	active	80
2807	1	\N	\N	active	81
2808	1	\N	\N	active	82
2809	1	\N	\N	active	83
2810	1	\N	\N	active	84
2811	1	\N	\N	active	85
2812	1	\N	\N	active	86
2813	1	\N	\N	active	87
2814	1	\N	\N	active	88
2815	1	\N	\N	active	89
2816	1	\N	\N	active	90
2817	1	\N	\N	active	91
2818	1	\N	\N	active	92
2819	1	\N	\N	active	93
2820	1	\N	\N	active	94
2821	1	\N	\N	active	95
2822	1	\N	\N	active	96
2823	1	\N	\N	active	97
2824	1	\N	\N	active	98
2825	1	\N	\N	active	99
2826	1	\N	\N	active	100
2827	1	\N	\N	active	101
2828	1	\N	\N	active	102
2829	1	\N	\N	active	103
2830	1	\N	\N	active	104
2831	1	\N	\N	active	105
2832	1	\N	\N	active	106
2833	1	\N	\N	active	107
2834	1	\N	\N	active	108
2835	1	\N	\N	active	109
2836	1	\N	\N	active	110
2837	1	\N	\N	active	111
2838	1	\N	\N	active	112
2839	1	\N	\N	active	113
2840	1	\N	\N	active	114
2841	1	\N	\N	active	115
2842	1	\N	\N	active	116
2843	1	\N	\N	active	117
2844	1	\N	\N	active	118
2845	1	\N	\N	active	119
2846	1	\N	\N	active	120
2847	1	\N	\N	active	121
2848	1	\N	\N	active	122
2849	1	\N	\N	active	123
2850	1	\N	\N	active	124
2851	1	\N	\N	active	125
2852	1	\N	\N	active	126
2853	1	\N	\N	active	127
2854	1	\N	\N	active	128
2855	1	\N	\N	active	129
2856	1	\N	\N	active	130
2857	1	\N	\N	active	131
2858	1	\N	\N	active	132
2859	1	\N	\N	active	133
2860	1	\N	\N	active	134
2861	1	\N	\N	active	135
2862	1	\N	\N	active	136
2863	1	\N	\N	active	137
2864	1	\N	\N	active	138
2865	1	\N	\N	active	139
2866	1	\N	\N	active	140
2867	1	\N	\N	active	141
2868	1	\N	\N	active	142
2869	1	\N	\N	active	143
2870	1	\N	\N	active	144
2871	1	\N	\N	active	145
2872	1	\N	\N	active	146
2873	1	\N	\N	active	147
2874	1	\N	\N	active	148
2875	1	\N	\N	active	149
2876	1	\N	\N	active	150
2877	1	\N	\N	active	151
2878	1	\N	\N	active	152
2879	1	\N	\N	active	153
2880	1	\N	\N	active	154
2881	1	\N	\N	active	155
2882	1	\N	\N	active	156
2883	1	\N	\N	active	157
2884	1	\N	\N	active	158
2885	1	\N	\N	active	159
2886	1	\N	\N	active	160
2887	1	\N	\N	active	161
2888	1	\N	\N	active	162
2889	1	\N	\N	active	163
2890	1	\N	\N	active	164
2891	1	\N	\N	active	165
2892	1	\N	\N	active	166
2893	1	\N	\N	active	167
2894	1	\N	\N	active	168
2895	1	\N	\N	active	169
2896	1	\N	\N	active	170
2897	1	\N	\N	active	171
2898	1	\N	\N	active	172
2899	1	\N	\N	active	173
2900	1	\N	\N	active	174
2901	1	\N	\N	active	175
2902	1	\N	\N	active	176
2903	1	\N	\N	active	177
2904	1	\N	\N	active	178
2905	1	\N	\N	active	179
2906	1	\N	\N	active	180
2907	1	\N	\N	active	181
2908	1	\N	\N	active	182
2909	1	\N	\N	active	183
2910	1	\N	\N	active	184
2911	1	\N	\N	active	185
2912	1	\N	\N	active	186
2913	1	\N	\N	active	187
2914	1	\N	\N	active	188
2915	1	\N	\N	active	189
2916	1	\N	\N	active	190
2917	1	\N	\N	active	191
2918	1	\N	\N	active	192
2919	1	\N	\N	active	193
2920	1	\N	\N	active	194
2921	1	\N	\N	active	195
2922	1	\N	\N	active	196
2923	1	\N	\N	active	197
2924	1	\N	\N	active	198
2925	1	\N	\N	active	199
2926	1	\N	\N	active	200
2927	1	\N	\N	active	201
2928	1	\N	\N	active	202
2929	1	\N	\N	active	203
2930	1	\N	\N	active	204
2931	1	\N	\N	active	205
2932	1	\N	\N	active	206
2933	1	\N	\N	active	207
2934	1	\N	\N	active	208
2935	1	\N	\N	active	209
2936	1	\N	\N	active	210
2937	1	\N	\N	active	211
2938	1	\N	\N	active	212
2939	1	\N	\N	active	213
2940	1	\N	\N	active	214
2941	1	\N	\N	active	215
2942	1	\N	\N	active	216
2943	1	\N	\N	active	217
2944	1	\N	\N	active	218
2945	1	\N	\N	active	219
2946	1	\N	\N	active	220
2947	1	\N	\N	active	221
2948	1	\N	\N	active	222
2949	1	\N	\N	active	223
2950	1	\N	\N	active	224
2951	1	\N	\N	active	225
2952	1	\N	\N	active	226
2953	1	\N	\N	active	227
2954	1	\N	\N	active	228
2955	1	\N	\N	active	229
2956	1	\N	\N	active	230
2957	1	\N	\N	active	231
2958	1	\N	\N	active	232
2959	1	\N	\N	active	233
2960	1	\N	\N	active	234
2961	1	\N	\N	active	235
2962	1	\N	\N	active	236
2963	1	\N	\N	active	237
2964	1	\N	\N	active	238
2965	1	\N	\N	active	239
2966	1	\N	\N	active	240
2967	1	\N	\N	active	241
2968	1	\N	\N	active	242
2969	1	\N	\N	active	243
2970	1	\N	\N	active	244
2971	1	\N	\N	active	245
2972	1	\N	\N	active	246
2973	1	\N	\N	active	247
2974	1	\N	\N	active	248
2975	1	\N	\N	active	249
2976	1	\N	\N	active	250
2977	1	\N	\N	active	251
2978	1	\N	\N	active	252
2979	1	\N	\N	active	253
2980	1	\N	\N	active	254
2981	1	\N	\N	active	255
2982	1	\N	\N	active	256
2983	1	\N	\N	active	257
2984	1	\N	\N	active	258
2985	1	\N	\N	active	259
2986	1	\N	\N	active	260
2987	1	\N	\N	active	261
2988	1	\N	\N	active	262
2989	1	\N	\N	active	263
2990	1	\N	\N	active	264
2991	1	\N	\N	active	265
2992	1	\N	\N	active	266
2993	1	\N	\N	active	267
2994	1	\N	\N	active	268
2995	1	\N	\N	active	269
2996	1	\N	\N	active	270
2997	1	\N	\N	active	271
2998	1	\N	\N	active	272
2999	1	\N	\N	active	273
3000	1	\N	\N	active	274
3001	1	\N	\N	active	275
3002	1	\N	\N	active	276
3003	1	\N	\N	active	277
3004	1	\N	\N	active	278
3005	1	\N	\N	active	279
3006	1	\N	\N	active	280
3007	1	\N	\N	active	281
3008	1	\N	\N	active	282
3009	1	\N	\N	active	283
3010	1	\N	\N	active	284
3011	1	\N	\N	active	285
3012	1	\N	\N	active	286
3013	1	\N	\N	active	287
3014	1	\N	\N	active	288
3015	1	\N	\N	active	289
3016	1	\N	\N	active	290
3017	1	\N	\N	active	291
3018	1	\N	\N	active	292
3019	1	\N	\N	active	293
3020	1	\N	\N	active	294
3021	1	\N	\N	active	295
3022	1	\N	\N	active	296
3023	1	\N	\N	active	297
3024	1	\N	\N	active	298
3025	1	\N	\N	active	299
3026	1	\N	\N	active	300
3228	1	\N	\N	active	201
3229	1	\N	\N	active	202
3230	1	\N	\N	active	203
3231	1	\N	\N	active	204
3232	1	\N	\N	active	205
3233	1	\N	\N	active	206
3234	1	\N	\N	active	207
3235	1	\N	\N	active	208
3236	1	\N	\N	active	209
3237	1	\N	\N	active	210
3238	1	\N	\N	active	211
3239	1	\N	\N	active	212
3240	1	\N	\N	active	213
3027	1	\N	\N	active	0
3028	1	\N	\N	active	1
3029	1	\N	\N	active	2
3030	1	\N	\N	active	3
3031	1	\N	\N	active	4
3032	1	\N	\N	active	5
3033	1	\N	\N	active	6
3034	1	\N	\N	active	7
3035	1	\N	\N	active	8
3036	1	\N	\N	active	9
3037	1	\N	\N	active	10
3038	1	\N	\N	active	11
3039	1	\N	\N	active	12
3040	1	\N	\N	active	13
3041	1	\N	\N	active	14
3042	1	\N	\N	active	15
3043	1	\N	\N	active	16
3044	1	\N	\N	active	17
3045	1	\N	\N	active	18
3046	1	\N	\N	active	19
3047	1	\N	\N	active	20
3048	1	\N	\N	active	21
3049	1	\N	\N	active	22
3050	1	\N	\N	active	23
3051	1	\N	\N	active	24
3052	1	\N	\N	active	25
3053	1	\N	\N	active	26
3054	1	\N	\N	active	27
3055	1	\N	\N	active	28
3056	1	\N	\N	active	29
3057	1	\N	\N	active	30
3058	1	\N	\N	active	31
3059	1	\N	\N	active	32
3060	1	\N	\N	active	33
3061	1	\N	\N	active	34
3062	1	\N	\N	active	35
3063	1	\N	\N	active	36
3064	1	\N	\N	active	37
3065	1	\N	\N	active	38
3066	1	\N	\N	active	39
3067	1	\N	\N	active	40
3068	1	\N	\N	active	41
3069	1	\N	\N	active	42
3070	1	\N	\N	active	43
3071	1	\N	\N	active	44
3072	1	\N	\N	active	45
3073	1	\N	\N	active	46
3074	1	\N	\N	active	47
3075	1	\N	\N	active	48
3076	1	\N	\N	active	49
3077	1	\N	\N	active	50
3078	1	\N	\N	active	51
3079	1	\N	\N	active	52
3080	1	\N	\N	active	53
3081	1	\N	\N	active	54
3082	1	\N	\N	active	55
3083	1	\N	\N	active	56
3084	1	\N	\N	active	57
3085	1	\N	\N	active	58
3086	1	\N	\N	active	59
3087	1	\N	\N	active	60
3088	1	\N	\N	active	61
3089	1	\N	\N	active	62
3090	1	\N	\N	active	63
3091	1	\N	\N	active	64
3092	1	\N	\N	active	65
3093	1	\N	\N	active	66
3094	1	\N	\N	active	67
3095	1	\N	\N	active	68
3096	1	\N	\N	active	69
3097	1	\N	\N	active	70
3098	1	\N	\N	active	71
3099	1	\N	\N	active	72
3100	1	\N	\N	active	73
3101	1	\N	\N	active	74
3102	1	\N	\N	active	75
3103	1	\N	\N	active	76
3104	1	\N	\N	active	77
3105	1	\N	\N	active	78
3106	1	\N	\N	active	79
3107	1	\N	\N	active	80
3108	1	\N	\N	active	81
3109	1	\N	\N	active	82
3110	1	\N	\N	active	83
3111	1	\N	\N	active	84
3112	1	\N	\N	active	85
3113	1	\N	\N	active	86
3114	1	\N	\N	active	87
3115	1	\N	\N	active	88
3116	1	\N	\N	active	89
3117	1	\N	\N	active	90
3118	1	\N	\N	active	91
3119	1	\N	\N	active	92
3120	1	\N	\N	active	93
3121	1	\N	\N	active	94
3122	1	\N	\N	active	95
3123	1	\N	\N	active	96
3124	1	\N	\N	active	97
3125	1	\N	\N	active	98
3126	1	\N	\N	active	99
3127	1	\N	\N	active	100
3128	1	\N	\N	active	101
3129	1	\N	\N	active	102
3130	1	\N	\N	active	103
3131	1	\N	\N	active	104
3132	1	\N	\N	active	105
3133	1	\N	\N	active	106
3134	1	\N	\N	active	107
3135	1	\N	\N	active	108
3136	1	\N	\N	active	109
3137	1	\N	\N	active	110
3138	1	\N	\N	active	111
3139	1	\N	\N	active	112
3140	1	\N	\N	active	113
3141	1	\N	\N	active	114
3142	1	\N	\N	active	115
3143	1	\N	\N	active	116
3144	1	\N	\N	active	117
3145	1	\N	\N	active	118
3146	1	\N	\N	active	119
3147	1	\N	\N	active	120
3148	1	\N	\N	active	121
3149	1	\N	\N	active	122
3150	1	\N	\N	active	123
3151	1	\N	\N	active	124
3152	1	\N	\N	active	125
3153	1	\N	\N	active	126
3154	1	\N	\N	active	127
3155	1	\N	\N	active	128
3156	1	\N	\N	active	129
3157	1	\N	\N	active	130
3158	1	\N	\N	active	131
3159	1	\N	\N	active	132
3160	1	\N	\N	active	133
3161	1	\N	\N	active	134
3162	1	\N	\N	active	135
3163	1	\N	\N	active	136
3164	1	\N	\N	active	137
3165	1	\N	\N	active	138
3166	1	\N	\N	active	139
3167	1	\N	\N	active	140
3168	1	\N	\N	active	141
3169	1	\N	\N	active	142
3170	1	\N	\N	active	143
3171	1	\N	\N	active	144
3172	1	\N	\N	active	145
3173	1	\N	\N	active	146
3174	1	\N	\N	active	147
3175	1	\N	\N	active	148
3176	1	\N	\N	active	149
3177	1	\N	\N	active	150
3178	1	\N	\N	active	151
3179	1	\N	\N	active	152
3180	1	\N	\N	active	153
3181	1	\N	\N	active	154
3182	1	\N	\N	active	155
3183	1	\N	\N	active	156
1522	1	\N	\N	active	0
1523	1	\N	\N	active	1
1524	1	\N	\N	active	2
1525	1	\N	\N	active	3
1526	1	\N	\N	active	4
1527	1	\N	\N	active	5
1528	1	\N	\N	active	6
1529	1	\N	\N	active	7
1530	1	\N	\N	active	8
1531	1	\N	\N	active	9
1532	1	\N	\N	active	10
1533	1	\N	\N	active	11
1534	1	\N	\N	active	12
1535	1	\N	\N	active	13
1536	1	\N	\N	active	14
1537	1	\N	\N	active	15
1538	1	\N	\N	active	16
1539	1	\N	\N	active	17
1540	1	\N	\N	active	18
1541	1	\N	\N	active	19
1542	1	\N	\N	active	20
1543	1	\N	\N	active	21
1544	1	\N	\N	active	22
1545	1	\N	\N	active	23
1546	1	\N	\N	active	24
1547	1	\N	\N	active	25
1548	1	\N	\N	active	26
1549	1	\N	\N	active	27
1550	1	\N	\N	active	28
1551	1	\N	\N	active	29
1552	1	\N	\N	active	30
1553	1	\N	\N	active	31
1554	1	\N	\N	active	32
1555	1	\N	\N	active	33
1556	1	\N	\N	active	34
1557	1	\N	\N	active	35
1558	1	\N	\N	active	36
1559	1	\N	\N	active	37
1560	1	\N	\N	active	38
1561	1	\N	\N	active	39
1562	1	\N	\N	active	40
1563	1	\N	\N	active	41
1564	1	\N	\N	active	42
1565	1	\N	\N	active	43
1566	1	\N	\N	active	44
1567	1	\N	\N	active	45
1568	1	\N	\N	active	46
1569	1	\N	\N	active	47
1570	1	\N	\N	active	48
1571	1	\N	\N	active	49
1572	1	\N	\N	active	50
1573	1	\N	\N	active	51
1574	1	\N	\N	active	52
1575	1	\N	\N	active	53
1576	1	\N	\N	active	54
1577	1	\N	\N	active	55
1578	1	\N	\N	active	56
1579	1	\N	\N	active	57
1580	1	\N	\N	active	58
1581	1	\N	\N	active	59
1582	1	\N	\N	active	60
1583	1	\N	\N	active	61
1584	1	\N	\N	active	62
1585	1	\N	\N	active	63
1586	1	\N	\N	active	64
1587	1	\N	\N	active	65
1588	1	\N	\N	active	66
1589	1	\N	\N	active	67
1590	1	\N	\N	active	68
1591	1	\N	\N	active	69
1592	1	\N	\N	active	70
1593	1	\N	\N	active	71
1594	1	\N	\N	active	72
1595	1	\N	\N	active	73
1596	1	\N	\N	active	74
1597	1	\N	\N	active	75
1598	1	\N	\N	active	76
1599	1	\N	\N	active	77
1600	1	\N	\N	active	78
1601	1	\N	\N	active	79
1602	1	\N	\N	active	80
1603	1	\N	\N	active	81
1604	1	\N	\N	active	82
1605	1	\N	\N	active	83
1606	1	\N	\N	active	84
1607	1	\N	\N	active	85
1608	1	\N	\N	active	86
1609	1	\N	\N	active	87
1610	1	\N	\N	active	88
1611	1	\N	\N	active	89
1612	1	\N	\N	active	90
1613	1	\N	\N	active	91
1614	1	\N	\N	active	92
1615	1	\N	\N	active	93
1616	1	\N	\N	active	94
1617	1	\N	\N	active	95
1618	1	\N	\N	active	96
1619	1	\N	\N	active	97
1620	1	\N	\N	active	98
1621	1	\N	\N	active	99
1622	1	\N	\N	active	100
1623	1	\N	\N	active	101
1624	1	\N	\N	active	102
1625	1	\N	\N	active	103
1626	1	\N	\N	active	104
1627	1	\N	\N	active	105
1628	1	\N	\N	active	106
1629	1	\N	\N	active	107
1630	1	\N	\N	active	108
1631	1	\N	\N	active	109
1632	1	\N	\N	active	110
1633	1	\N	\N	active	111
1634	1	\N	\N	active	112
1635	1	\N	\N	active	113
1636	1	\N	\N	active	114
1637	1	\N	\N	active	115
1638	1	\N	\N	active	116
1639	1	\N	\N	active	117
1640	1	\N	\N	active	118
1641	1	\N	\N	active	119
1642	1	\N	\N	active	120
1643	1	\N	\N	active	121
1644	1	\N	\N	active	122
1645	1	\N	\N	active	123
1646	1	\N	\N	active	124
1647	1	\N	\N	active	125
1648	1	\N	\N	active	126
1649	1	\N	\N	active	127
1650	1	\N	\N	active	128
1651	1	\N	\N	active	129
1652	1	\N	\N	active	130
1653	1	\N	\N	active	131
1654	1	\N	\N	active	132
1655	1	\N	\N	active	133
1656	1	\N	\N	active	134
1657	1	\N	\N	active	135
1658	1	\N	\N	active	136
1659	1	\N	\N	active	137
1660	1	\N	\N	active	138
1661	1	\N	\N	active	139
1662	1	\N	\N	active	140
1663	1	\N	\N	active	141
1664	1	\N	\N	active	142
1665	1	\N	\N	active	143
1666	1	\N	\N	active	144
1667	1	\N	\N	active	145
1668	1	\N	\N	active	146
1669	1	\N	\N	active	147
1670	1	\N	\N	active	148
1671	1	\N	\N	active	149
1672	1	\N	\N	active	150
1673	1	\N	\N	active	151
1674	1	\N	\N	active	152
1675	1	\N	\N	active	153
1676	1	\N	\N	active	154
1677	1	\N	\N	active	155
1678	1	\N	\N	active	156
1679	1	\N	\N	active	157
1680	1	\N	\N	active	158
1681	1	\N	\N	active	159
1682	1	\N	\N	active	160
1683	1	\N	\N	active	161
1684	1	\N	\N	active	162
1685	1	\N	\N	active	163
1686	1	\N	\N	active	164
1687	1	\N	\N	active	165
1688	1	\N	\N	active	166
1689	1	\N	\N	active	167
1690	1	\N	\N	active	168
1691	1	\N	\N	active	169
1692	1	\N	\N	active	170
1693	1	\N	\N	active	171
1694	1	\N	\N	active	172
1695	1	\N	\N	active	173
1696	1	\N	\N	active	174
1697	1	\N	\N	active	175
1698	1	\N	\N	active	176
1699	1	\N	\N	active	177
1700	1	\N	\N	active	178
1701	1	\N	\N	active	179
1702	1	\N	\N	active	180
1703	1	\N	\N	active	181
1704	1	\N	\N	active	182
1705	1	\N	\N	active	183
1706	1	\N	\N	active	184
1707	1	\N	\N	active	185
1708	1	\N	\N	active	186
1709	1	\N	\N	active	187
1710	1	\N	\N	active	188
1711	1	\N	\N	active	189
1712	1	\N	\N	active	190
1713	1	\N	\N	active	191
1714	1	\N	\N	active	192
1715	1	\N	\N	active	193
1716	1	\N	\N	active	194
1717	1	\N	\N	active	195
1718	1	\N	\N	active	196
1719	1	\N	\N	active	197
1720	1	\N	\N	active	198
1721	1	\N	\N	active	199
1722	1	\N	\N	active	200
1723	1	\N	\N	active	201
1724	1	\N	\N	active	202
1725	1	\N	\N	active	203
1726	1	\N	\N	active	204
1727	1	\N	\N	active	205
1728	1	\N	\N	active	206
1729	1	\N	\N	active	207
1730	1	\N	\N	active	208
1731	1	\N	\N	active	209
1732	1	\N	\N	active	210
1733	1	\N	\N	active	211
1734	1	\N	\N	active	212
1735	1	\N	\N	active	213
1736	1	\N	\N	active	214
1737	1	\N	\N	active	215
1738	1	\N	\N	active	216
1739	1	\N	\N	active	217
1740	1	\N	\N	active	218
1741	1	\N	\N	active	219
1742	1	\N	\N	active	220
1743	1	\N	\N	active	221
1744	1	\N	\N	active	222
1745	1	\N	\N	active	223
1746	1	\N	\N	active	224
1747	1	\N	\N	active	225
1748	1	\N	\N	active	226
1749	1	\N	\N	active	227
1750	1	\N	\N	active	228
1751	1	\N	\N	active	229
1752	1	\N	\N	active	230
1753	1	\N	\N	active	231
1754	1	\N	\N	active	232
1755	1	\N	\N	active	233
1756	1	\N	\N	active	234
1757	1	\N	\N	active	235
1758	1	\N	\N	active	236
1759	1	\N	\N	active	237
1760	1	\N	\N	active	238
1761	1	\N	\N	active	239
1762	1	\N	\N	active	240
1763	1	\N	\N	active	241
1764	1	\N	\N	active	242
1765	1	\N	\N	active	243
1766	1	\N	\N	active	244
1767	1	\N	\N	active	245
1768	1	\N	\N	active	246
1769	1	\N	\N	active	247
1770	1	\N	\N	active	248
1771	1	\N	\N	active	249
1772	1	\N	\N	active	250
1773	1	\N	\N	active	251
1774	1	\N	\N	active	252
1775	1	\N	\N	active	253
1776	1	\N	\N	active	254
1777	1	\N	\N	active	255
1778	1	\N	\N	active	256
1779	1	\N	\N	active	257
1780	1	\N	\N	active	258
1781	1	\N	\N	active	259
1782	1	\N	\N	active	260
1783	1	\N	\N	active	261
1784	1	\N	\N	active	262
1785	1	\N	\N	active	263
1786	1	\N	\N	active	264
1787	1	\N	\N	active	265
1788	1	\N	\N	active	266
1789	1	\N	\N	active	267
1790	1	\N	\N	active	268
1791	1	\N	\N	active	269
1792	1	\N	\N	active	270
1793	1	\N	\N	active	271
1794	1	\N	\N	active	272
1795	1	\N	\N	active	273
1796	1	\N	\N	active	274
1797	1	\N	\N	active	275
1798	1	\N	\N	active	276
1799	1	\N	\N	active	277
1800	1	\N	\N	active	278
1801	1	\N	\N	active	279
1802	1	\N	\N	active	280
1803	1	\N	\N	active	281
1804	1	\N	\N	active	282
1805	1	\N	\N	active	283
1806	1	\N	\N	active	284
1807	1	\N	\N	active	285
1808	1	\N	\N	active	286
1809	1	\N	\N	active	287
1810	1	\N	\N	active	288
1811	1	\N	\N	active	289
1812	1	\N	\N	active	290
1813	1	\N	\N	active	291
1814	1	\N	\N	active	292
1815	1	\N	\N	active	293
1816	1	\N	\N	active	294
1817	1	\N	\N	active	295
1818	1	\N	\N	active	296
1819	1	\N	\N	active	297
1820	1	\N	\N	active	298
1821	1	\N	\N	active	299
1822	1	\N	\N	active	300
3184	1	\N	\N	active	157
3185	1	\N	\N	active	158
3186	1	\N	\N	active	159
3187	1	\N	\N	active	160
3188	1	\N	\N	active	161
3241	1	\N	\N	active	214
3242	1	\N	\N	active	215
3243	1	\N	\N	active	216
3244	1	\N	\N	active	217
3245	1	\N	\N	active	218
3246	1	\N	\N	active	219
3247	1	\N	\N	active	220
3248	1	\N	\N	active	221
3249	1	\N	\N	active	222
3250	1	\N	\N	active	223
3251	1	\N	\N	active	224
3252	1	\N	\N	active	225
3253	1	\N	\N	active	226
3254	1	\N	\N	active	227
3255	1	\N	\N	active	228
3256	1	\N	\N	active	229
3257	1	\N	\N	active	230
3258	1	\N	\N	active	231
3259	1	\N	\N	active	232
3260	1	\N	\N	active	233
3261	1	\N	\N	active	234
3262	1	\N	\N	active	235
3263	1	\N	\N	active	236
3264	1	\N	\N	active	237
3265	1	\N	\N	active	238
3266	1	\N	\N	active	239
3267	1	\N	\N	active	240
3268	1	\N	\N	active	241
3269	1	\N	\N	active	242
3270	1	\N	\N	active	243
3271	1	\N	\N	active	244
3272	1	\N	\N	active	245
3273	1	\N	\N	active	246
3274	1	\N	\N	active	247
3275	1	\N	\N	active	248
3276	1	\N	\N	active	249
3277	1	\N	\N	active	250
3278	1	\N	\N	active	251
3279	1	\N	\N	active	252
3280	1	\N	\N	active	253
3281	1	\N	\N	active	254
3282	1	\N	\N	active	255
3283	1	\N	\N	active	256
3284	1	\N	\N	active	257
3285	1	\N	\N	active	258
3286	1	\N	\N	active	259
3287	1	\N	\N	active	260
3288	1	\N	\N	active	261
3289	1	\N	\N	active	262
3290	1	\N	\N	active	263
3291	1	\N	\N	active	264
3292	1	\N	\N	active	265
3293	1	\N	\N	active	266
3294	1	\N	\N	active	267
3295	1	\N	\N	active	268
3296	1	\N	\N	active	269
3297	1	\N	\N	active	270
3298	1	\N	\N	active	271
3299	1	\N	\N	active	272
3300	1	\N	\N	active	273
3301	1	\N	\N	active	274
3302	1	\N	\N	active	275
3303	1	\N	\N	active	276
3304	1	\N	\N	active	277
3305	1	\N	\N	active	278
3306	1	\N	\N	active	279
3307	1	\N	\N	active	280
3308	1	\N	\N	active	281
3309	1	\N	\N	active	282
3310	1	\N	\N	active	283
3311	1	\N	\N	active	284
3312	1	\N	\N	active	285
3313	1	\N	\N	active	286
3314	1	\N	\N	active	287
3315	1	\N	\N	active	288
3316	1	\N	\N	active	289
3317	1	\N	\N	active	290
3318	1	\N	\N	active	291
3319	1	\N	\N	active	292
3320	1	\N	\N	active	293
3321	1	\N	\N	active	294
3322	1	\N	\N	active	295
3323	1	\N	\N	active	296
3324	1	\N	\N	active	297
3325	1	\N	\N	active	298
3326	1	\N	\N	active	299
3327	1	\N	\N	active	300
3328	1	\N	\N	active	0
3329	1	\N	\N	active	1
3330	1	\N	\N	active	2
3331	1	\N	\N	active	3
3332	1	\N	\N	active	4
3333	1	\N	\N	active	5
3334	1	\N	\N	active	6
3335	1	\N	\N	active	7
3336	1	\N	\N	active	8
3337	1	\N	\N	active	9
3338	1	\N	\N	active	10
3339	1	\N	\N	active	11
3340	1	\N	\N	active	12
3341	1	\N	\N	active	13
3342	1	\N	\N	active	14
3343	1	\N	\N	active	15
3344	1	\N	\N	active	16
3345	1	\N	\N	active	17
3346	1	\N	\N	active	18
3347	1	\N	\N	active	19
3348	1	\N	\N	active	20
3349	1	\N	\N	active	21
3350	1	\N	\N	active	22
3351	1	\N	\N	active	23
3352	1	\N	\N	active	24
3353	1	\N	\N	active	25
3354	1	\N	\N	active	26
3355	1	\N	\N	active	27
3356	1	\N	\N	active	28
3357	1	\N	\N	active	29
3358	1	\N	\N	active	30
3359	1	\N	\N	active	31
3360	1	\N	\N	active	32
3361	1	\N	\N	active	33
3362	1	\N	\N	active	34
3363	1	\N	\N	active	35
3364	1	\N	\N	active	36
3365	1	\N	\N	active	37
3366	1	\N	\N	active	38
3367	1	\N	\N	active	39
3368	1	\N	\N	active	40
3369	1	\N	\N	active	41
3370	1	\N	\N	active	42
3371	1	\N	\N	active	43
3372	1	\N	\N	active	44
3373	1	\N	\N	active	45
3374	1	\N	\N	active	46
3375	1	\N	\N	active	47
3376	1	\N	\N	active	48
3377	1	\N	\N	active	49
3378	1	\N	\N	active	50
3379	1	\N	\N	active	51
3380	1	\N	\N	active	52
3381	1	\N	\N	active	53
3382	1	\N	\N	active	54
3383	1	\N	\N	active	55
3384	1	\N	\N	active	56
3385	1	\N	\N	active	57
3386	1	\N	\N	active	58
3387	1	\N	\N	active	59
3388	1	\N	\N	active	60
3389	1	\N	\N	active	61
3390	1	\N	\N	active	62
3391	1	\N	\N	active	63
3392	1	\N	\N	active	64
3393	1	\N	\N	active	65
3394	1	\N	\N	active	66
3395	1	\N	\N	active	67
3396	1	\N	\N	active	68
3397	1	\N	\N	active	69
3398	1	\N	\N	active	70
3399	1	\N	\N	active	71
3400	1	\N	\N	active	72
3401	1	\N	\N	active	73
3402	1	\N	\N	active	74
3403	1	\N	\N	active	75
3404	1	\N	\N	active	76
3405	1	\N	\N	active	77
3406	1	\N	\N	active	78
3407	1	\N	\N	active	79
3408	1	\N	\N	active	80
3409	1	\N	\N	active	81
3410	1	\N	\N	active	82
3411	1	\N	\N	active	83
3412	1	\N	\N	active	84
3413	1	\N	\N	active	85
3414	1	\N	\N	active	86
3415	1	\N	\N	active	87
3416	1	\N	\N	active	88
3417	1	\N	\N	active	89
3418	1	\N	\N	active	90
3419	1	\N	\N	active	91
3420	1	\N	\N	active	92
3421	1	\N	\N	active	93
3422	1	\N	\N	active	94
3423	1	\N	\N	active	95
3424	1	\N	\N	active	96
3425	1	\N	\N	active	97
3426	1	\N	\N	active	98
3427	1	\N	\N	active	99
3428	1	\N	\N	active	100
3429	1	\N	\N	active	101
3430	1	\N	\N	active	102
3431	1	\N	\N	active	103
3432	1	\N	\N	active	104
3433	1	\N	\N	active	105
3434	1	\N	\N	active	106
3435	1	\N	\N	active	107
3436	1	\N	\N	active	108
3437	1	\N	\N	active	109
3438	1	\N	\N	active	110
3439	1	\N	\N	active	111
3440	1	\N	\N	active	112
3441	1	\N	\N	active	113
3442	1	\N	\N	active	114
3443	1	\N	\N	active	115
3444	1	\N	\N	active	116
3445	1	\N	\N	active	117
3446	1	\N	\N	active	118
3447	1	\N	\N	active	119
3448	1	\N	\N	active	120
3449	1	\N	\N	active	121
3450	1	\N	\N	active	122
3451	1	\N	\N	active	123
3452	1	\N	\N	active	124
3453	1	\N	\N	active	125
3454	1	\N	\N	active	126
3455	1	\N	\N	active	127
3456	1	\N	\N	active	128
3457	1	\N	\N	active	129
3458	1	\N	\N	active	130
3459	1	\N	\N	active	131
3460	1	\N	\N	active	132
3461	1	\N	\N	active	133
3462	1	\N	\N	active	134
3463	1	\N	\N	active	135
3464	1	\N	\N	active	136
3465	1	\N	\N	active	137
3466	1	\N	\N	active	138
3467	1	\N	\N	active	139
3468	1	\N	\N	active	140
3469	1	\N	\N	active	141
3470	1	\N	\N	active	142
3471	1	\N	\N	active	143
3472	1	\N	\N	active	144
3473	1	\N	\N	active	145
3474	1	\N	\N	active	146
3475	1	\N	\N	active	147
3476	1	\N	\N	active	148
3477	1	\N	\N	active	149
3478	1	\N	\N	active	150
3479	1	\N	\N	active	151
3480	1	\N	\N	active	152
3481	1	\N	\N	active	153
3482	1	\N	\N	active	154
3483	1	\N	\N	active	155
3484	1	\N	\N	active	156
3485	1	\N	\N	active	157
3486	1	\N	\N	active	158
3487	1	\N	\N	active	159
3488	1	\N	\N	active	160
3489	1	\N	\N	active	161
3490	1	\N	\N	active	162
3491	1	\N	\N	active	163
3492	1	\N	\N	active	164
3493	1	\N	\N	active	165
3494	1	\N	\N	active	166
3495	1	\N	\N	active	167
3496	1	\N	\N	active	168
3497	1	\N	\N	active	169
3498	1	\N	\N	active	170
3499	1	\N	\N	active	171
3500	1	\N	\N	active	172
3501	1	\N	\N	active	173
3502	1	\N	\N	active	174
3503	1	\N	\N	active	175
3504	1	\N	\N	active	176
3505	1	\N	\N	active	177
3506	1	\N	\N	active	178
3507	1	\N	\N	active	179
3508	1	\N	\N	active	180
3509	1	\N	\N	active	181
3510	1	\N	\N	active	182
3511	1	\N	\N	active	183
3512	1	\N	\N	active	184
3513	1	\N	\N	active	185
3514	1	\N	\N	active	186
3515	1	\N	\N	active	187
3516	1	\N	\N	active	188
3517	1	\N	\N	active	189
3518	1	\N	\N	active	190
3519	1	\N	\N	active	191
3520	1	\N	\N	active	192
3521	1	\N	\N	active	193
3522	1	\N	\N	active	194
3523	1	\N	\N	active	195
3524	1	\N	\N	active	196
3525	1	\N	\N	active	197
3526	1	\N	\N	active	198
3527	1	\N	\N	active	199
3528	1	\N	\N	active	200
3529	1	\N	\N	active	201
3530	1	\N	\N	active	202
3531	1	\N	\N	active	203
3532	1	\N	\N	active	204
3533	1	\N	\N	active	205
3534	1	\N	\N	active	206
3535	1	\N	\N	active	207
3536	1	\N	\N	active	208
3537	1	\N	\N	active	209
3538	1	\N	\N	active	210
3539	1	\N	\N	active	211
3540	1	\N	\N	active	212
3541	1	\N	\N	active	213
3542	1	\N	\N	active	214
3543	1	\N	\N	active	215
3544	1	\N	\N	active	216
3545	1	\N	\N	active	217
3546	1	\N	\N	active	218
3547	1	\N	\N	active	219
3548	1	\N	\N	active	220
3549	1	\N	\N	active	221
3550	1	\N	\N	active	222
3551	1	\N	\N	active	223
3552	1	\N	\N	active	224
3553	1	\N	\N	active	225
3554	1	\N	\N	active	226
3555	1	\N	\N	active	227
3556	1	\N	\N	active	228
3557	1	\N	\N	active	229
3558	1	\N	\N	active	230
3559	1	\N	\N	active	231
3560	1	\N	\N	active	232
3561	1	\N	\N	active	233
3562	1	\N	\N	active	234
3563	1	\N	\N	active	235
3564	1	\N	\N	active	236
3565	1	\N	\N	active	237
3566	1	\N	\N	active	238
3567	1	\N	\N	active	239
3568	1	\N	\N	active	240
3569	1	\N	\N	active	241
3570	1	\N	\N	active	242
3571	1	\N	\N	active	243
3572	1	\N	\N	active	244
3573	1	\N	\N	active	245
3574	1	\N	\N	active	246
3575	1	\N	\N	active	247
3576	1	\N	\N	active	248
3577	1	\N	\N	active	249
3578	1	\N	\N	active	250
3579	1	\N	\N	active	251
3580	1	\N	\N	active	252
3581	1	\N	\N	active	253
3582	1	\N	\N	active	254
3583	1	\N	\N	active	255
3584	1	\N	\N	active	256
3585	1	\N	\N	active	257
3586	1	\N	\N	active	258
3587	1	\N	\N	active	259
3588	1	\N	\N	active	260
3589	1	\N	\N	active	261
3590	1	\N	\N	active	262
3591	1	\N	\N	active	263
3592	1	\N	\N	active	264
3593	1	\N	\N	active	265
3594	1	\N	\N	active	266
3595	1	\N	\N	active	267
3596	1	\N	\N	active	268
3597	1	\N	\N	active	269
3598	1	\N	\N	active	270
3599	1	\N	\N	active	271
3600	1	\N	\N	active	272
3601	1	\N	\N	active	273
3602	1	\N	\N	active	274
3603	1	\N	\N	active	275
3604	1	\N	\N	active	276
3605	1	\N	\N	active	277
3606	1	\N	\N	active	278
3607	1	\N	\N	active	279
3608	1	\N	\N	active	280
3609	1	\N	\N	active	281
3610	1	\N	\N	active	282
3611	1	\N	\N	active	283
3612	1	\N	\N	active	284
3613	1	\N	\N	active	285
3614	1	\N	\N	active	286
3615	1	\N	\N	active	287
3616	1	\N	\N	active	288
3617	1	\N	\N	active	289
3618	1	\N	\N	active	290
3619	1	\N	\N	active	291
3620	1	\N	\N	active	292
3621	1	\N	\N	active	293
3622	1	\N	\N	active	294
3623	1	\N	\N	active	295
3624	1	\N	\N	active	296
3625	1	\N	\N	active	297
3626	1	\N	\N	active	298
3627	1	\N	\N	active	299
3628	1	\N	\N	active	300
\.


--
-- Data for Name: SearchKeyword; Type: TABLE DATA; Schema: public; Owner: student
--

COPY public."SearchKeyword" (search_keyword_id, search_id, keyword_id) FROM stdin;
\.


--
-- Data for Name: SearchShare; Type: TABLE DATA; Schema: public; Owner: student
--

COPY public."SearchShare" (share_id, search_id, shared_with_user_id, shared_by_user_id, share_date) FROM stdin;
\.


--
-- Data for Name: Source; Type: TABLE DATA; Schema: public; Owner: student
--

COPY public."Source" (source_id, name, api_endpoint, scrape_source_url) FROM stdin;
1	Sample Source	https://www.sampleapi.com	https://scrapesource.com
2	Scopus	https://api.elsevier.com/content/search/scopus?	https://api.elsevier.com/
3	ScienceDirect	https://api.elsevier.com/content/search/sciencedirect?	https://api.elsevier.com/
\.


--
-- Data for Name: User; Type: TABLE DATA; Schema: public; Owner: student
--

COPY public."User" (user_id, username, password, role_id, email, registration_date) FROM stdin;
1	gAAAAABnMfRwVoDDWu_01sw0AzKrJHXm-43f7uZSClnu8qsiX_jmtGLATSnvZcgG-Bvm43nAJokeD73kYFVABMtM7mh3cuoJlg==	$2b$12$sNV0sctSpaWlxq6x/zEPSOkyn/30.TyIgqQFw5SrZ76E4Hh80kqTG	1	$2b$12$XFWdDCiLtwlP.E7rh.6.3OnR5GTvj7qq.nmEfzP0qQuMl/0e1C/RC	2024-11-11 12:11:28.768197
\.


--
-- Data for Name: UserData; Type: TABLE DATA; Schema: public; Owner: student
--

COPY public."UserData" (userdata_id, user_id, article_id, relevancy_color, methodology, clarity, transparency, completeness, evaluation_criteria) FROM stdin;
\.


--
-- Name: ArticleScore_article_score_id_seq; Type: SEQUENCE SET; Schema: public; Owner: student
--

SELECT pg_catalog.setval('public."ArticleScore_article_score_id_seq"', 1, false);


--
-- Name: Article_article_id_seq; Type: SEQUENCE SET; Schema: public; Owner: student
--

SELECT pg_catalog.setval('public."Article_article_id_seq"', 500, true);


--
-- Name: Collaboration_collaboration_id_seq; Type: SEQUENCE SET; Schema: public; Owner: student
--

SELECT pg_catalog.setval('public."Collaboration_collaboration_id_seq"', 1, false);


--
-- Name: Comment_comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: student
--

SELECT pg_catalog.setval('public."Comment_comment_id_seq"', 1, false);


--
-- Name: Keyword_keyword_id_seq; Type: SEQUENCE SET; Schema: public; Owner: student
--

SELECT pg_catalog.setval('public."Keyword_keyword_id_seq"', 13, true);


--
-- Name: ResearchQuestionMapping_research_question_mapping_id_seq; Type: SEQUENCE SET; Schema: public; Owner: student
--

SELECT pg_catalog.setval('public."ResearchQuestionMapping_research_question_mapping_id_seq"', 1, false);


--
-- Name: ResearchQuestionScore_research_question_score_id_seq; Type: SEQUENCE SET; Schema: public; Owner: student
--

SELECT pg_catalog.setval('public."ResearchQuestionScore_research_question_score_id_seq"', 1, false);


--
-- Name: ResearchQuestion_research_question_id_seq; Type: SEQUENCE SET; Schema: public; Owner: student
--

SELECT pg_catalog.setval('public."ResearchQuestion_research_question_id_seq"', 1, false);


--
-- Name: Role_role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: student
--

SELECT pg_catalog.setval('public."Role_role_id_seq"', 12, true);


--
-- Name: SearchKeyword_search_keyword_id_seq; Type: SEQUENCE SET; Schema: public; Owner: student
--

SELECT pg_catalog.setval('public."SearchKeyword_search_keyword_id_seq"', 1, false);


--
-- Name: SearchShare_share_id_seq; Type: SEQUENCE SET; Schema: public; Owner: student
--

SELECT pg_catalog.setval('public."SearchShare_share_id_seq"', 1, true);


--
-- Name: Search_search_id_seq; Type: SEQUENCE SET; Schema: public; Owner: student
--

SELECT pg_catalog.setval('public."Search_search_id_seq"', 4533, true);


--
-- Name: Source_source_id_seq; Type: SEQUENCE SET; Schema: public; Owner: student
--

SELECT pg_catalog.setval('public."Source_source_id_seq"', 13, true);


--
-- Name: UserData_userdata_id_seq; Type: SEQUENCE SET; Schema: public; Owner: student
--

SELECT pg_catalog.setval('public."UserData_userdata_id_seq"', 500, true);


--
-- Name: User_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: student
--

SELECT pg_catalog.setval('public."User_user_id_seq"', 24, true);


--
-- Name: ArticleScore ArticleScore_pkey; Type: CONSTRAINT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."ArticleScore"
    ADD CONSTRAINT "ArticleScore_pkey" PRIMARY KEY (article_score_id);


--
-- Name: Article Article_pkey; Type: CONSTRAINT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."Article"
    ADD CONSTRAINT "Article_pkey" PRIMARY KEY (article_id);


--
-- Name: Collaboration Collaboration_pkey; Type: CONSTRAINT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."Collaboration"
    ADD CONSTRAINT "Collaboration_pkey" PRIMARY KEY (collaboration_id);


--
-- Name: Comment Comment_pkey; Type: CONSTRAINT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."Comment"
    ADD CONSTRAINT "Comment_pkey" PRIMARY KEY (comment_id);


--
-- Name: Keyword Keyword_pkey; Type: CONSTRAINT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."Keyword"
    ADD CONSTRAINT "Keyword_pkey" PRIMARY KEY (keyword_id);


--
-- Name: ResearchQuestionMapping ResearchQuestionMapping_pkey; Type: CONSTRAINT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."ResearchQuestionMapping"
    ADD CONSTRAINT "ResearchQuestionMapping_pkey" PRIMARY KEY (research_question_mapping_id);


--
-- Name: ResearchQuestionScore ResearchQuestionScore_pkey; Type: CONSTRAINT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."ResearchQuestionScore"
    ADD CONSTRAINT "ResearchQuestionScore_pkey" PRIMARY KEY (research_question_score_id);


--
-- Name: ResearchQuestion ResearchQuestion_pkey; Type: CONSTRAINT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."ResearchQuestion"
    ADD CONSTRAINT "ResearchQuestion_pkey" PRIMARY KEY (research_question_id);


--
-- Name: Role Role_pkey; Type: CONSTRAINT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."Role"
    ADD CONSTRAINT "Role_pkey" PRIMARY KEY (role_id);


--
-- Name: Role Role_role_name_key; Type: CONSTRAINT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."Role"
    ADD CONSTRAINT "Role_role_name_key" UNIQUE (role_name);


--
-- Name: SearchKeyword SearchKeyword_pkey; Type: CONSTRAINT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."SearchKeyword"
    ADD CONSTRAINT "SearchKeyword_pkey" PRIMARY KEY (search_keyword_id);


--
-- Name: SearchShare SearchShare_pkey; Type: CONSTRAINT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."SearchShare"
    ADD CONSTRAINT "SearchShare_pkey" PRIMARY KEY (share_id);


--
-- Name: Search Search_pkey; Type: CONSTRAINT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."Search"
    ADD CONSTRAINT "Search_pkey" PRIMARY KEY (search_id);


--
-- Name: Source Source_pkey; Type: CONSTRAINT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."Source"
    ADD CONSTRAINT "Source_pkey" PRIMARY KEY (source_id);


--
-- Name: UserData UserData_pkey; Type: CONSTRAINT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."UserData"
    ADD CONSTRAINT "UserData_pkey" PRIMARY KEY (userdata_id);


--
-- Name: User User_email_key; Type: CONSTRAINT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."User"
    ADD CONSTRAINT "User_email_key" UNIQUE (email);


--
-- Name: User User_pkey; Type: CONSTRAINT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."User"
    ADD CONSTRAINT "User_pkey" PRIMARY KEY (user_id);


--
-- Name: User User_username_key; Type: CONSTRAINT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."User"
    ADD CONSTRAINT "User_username_key" UNIQUE (username);


--
-- Name: ix_ArticleScore_article_score_id; Type: INDEX; Schema: public; Owner: student
--

CREATE INDEX "ix_ArticleScore_article_score_id" ON public."ArticleScore" USING btree (article_score_id);


--
-- Name: ix_Article_article_id; Type: INDEX; Schema: public; Owner: student
--

CREATE INDEX "ix_Article_article_id" ON public."Article" USING btree (article_id);


--
-- Name: ix_Collaboration_collaboration_id; Type: INDEX; Schema: public; Owner: student
--

CREATE INDEX "ix_Collaboration_collaboration_id" ON public."Collaboration" USING btree (collaboration_id);


--
-- Name: ix_Comment_comment_id; Type: INDEX; Schema: public; Owner: student
--

CREATE INDEX "ix_Comment_comment_id" ON public."Comment" USING btree (comment_id);


--
-- Name: ix_Keyword_keyword_id; Type: INDEX; Schema: public; Owner: student
--

CREATE INDEX "ix_Keyword_keyword_id" ON public."Keyword" USING btree (keyword_id);


--
-- Name: ix_ResearchQuestionMapping_research_question_mapping_id; Type: INDEX; Schema: public; Owner: student
--

CREATE INDEX "ix_ResearchQuestionMapping_research_question_mapping_id" ON public."ResearchQuestionMapping" USING btree (research_question_mapping_id);


--
-- Name: ix_ResearchQuestionScore_research_question_score_id; Type: INDEX; Schema: public; Owner: student
--

CREATE INDEX "ix_ResearchQuestionScore_research_question_score_id" ON public."ResearchQuestionScore" USING btree (research_question_score_id);


--
-- Name: ix_ResearchQuestion_research_question_id; Type: INDEX; Schema: public; Owner: student
--

CREATE INDEX "ix_ResearchQuestion_research_question_id" ON public."ResearchQuestion" USING btree (research_question_id);


--
-- Name: ix_Role_role_id; Type: INDEX; Schema: public; Owner: student
--

CREATE INDEX "ix_Role_role_id" ON public."Role" USING btree (role_id);


--
-- Name: ix_SearchKeyword_search_keyword_id; Type: INDEX; Schema: public; Owner: student
--

CREATE INDEX "ix_SearchKeyword_search_keyword_id" ON public."SearchKeyword" USING btree (search_keyword_id);


--
-- Name: ix_SearchShare_share_id; Type: INDEX; Schema: public; Owner: student
--

CREATE INDEX "ix_SearchShare_share_id" ON public."SearchShare" USING btree (share_id);


--
-- Name: ix_Search_search_id; Type: INDEX; Schema: public; Owner: student
--

CREATE INDEX "ix_Search_search_id" ON public."Search" USING btree (search_id);


--
-- Name: ix_Source_source_id; Type: INDEX; Schema: public; Owner: student
--

CREATE INDEX "ix_Source_source_id" ON public."Source" USING btree (source_id);


--
-- Name: ix_UserData_userdata_id; Type: INDEX; Schema: public; Owner: student
--

CREATE INDEX "ix_UserData_userdata_id" ON public."UserData" USING btree (userdata_id);


--
-- Name: ix_User_user_id; Type: INDEX; Schema: public; Owner: student
--

CREATE INDEX "ix_User_user_id" ON public."User" USING btree (user_id);


--
-- Name: ArticleScore ArticleScore_article_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."ArticleScore"
    ADD CONSTRAINT "ArticleScore_article_id_fkey" FOREIGN KEY (article_id) REFERENCES public."Article"(article_id);


--
-- Name: ArticleScore ArticleScore_last_updated_by_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."ArticleScore"
    ADD CONSTRAINT "ArticleScore_last_updated_by_user_id_fkey" FOREIGN KEY (last_updated_by_user_id) REFERENCES public."User"(user_id);


--
-- Name: ArticleScore ArticleScore_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."ArticleScore"
    ADD CONSTRAINT "ArticleScore_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."User"(user_id);


--
-- Name: Article Article_search_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."Article"
    ADD CONSTRAINT "Article_search_id_fkey" FOREIGN KEY (search_id) REFERENCES public."Search"(search_id) ON DELETE CASCADE;


--
-- Name: Article Article_source_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."Article"
    ADD CONSTRAINT "Article_source_id_fkey" FOREIGN KEY (source_id) REFERENCES public."Source"(source_id) ON DELETE CASCADE;


--
-- Name: Article Article_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."Article"
    ADD CONSTRAINT "Article_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."User"(user_id) ON DELETE CASCADE;


--
-- Name: Collaboration Collaboration_article_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."Collaboration"
    ADD CONSTRAINT "Collaboration_article_id_fkey" FOREIGN KEY (article_id) REFERENCES public."Article"(article_id);


--
-- Name: Collaboration Collaboration_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."Collaboration"
    ADD CONSTRAINT "Collaboration_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."User"(user_id);


--
-- Name: Comment Comment_article_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."Comment"
    ADD CONSTRAINT "Comment_article_id_fkey" FOREIGN KEY (article_id) REFERENCES public."Article"(article_id) ON DELETE CASCADE;


--
-- Name: Comment Comment_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."Comment"
    ADD CONSTRAINT "Comment_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."User"(user_id) ON DELETE CASCADE;


--
-- Name: ResearchQuestionMapping ResearchQuestionMapping_article_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."ResearchQuestionMapping"
    ADD CONSTRAINT "ResearchQuestionMapping_article_id_fkey" FOREIGN KEY (article_id) REFERENCES public."Article"(article_id);


--
-- Name: ResearchQuestionMapping ResearchQuestionMapping_research_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."ResearchQuestionMapping"
    ADD CONSTRAINT "ResearchQuestionMapping_research_question_id_fkey" FOREIGN KEY (research_question_id) REFERENCES public."ResearchQuestion"(research_question_id);


--
-- Name: ResearchQuestionScore ResearchQuestionScore_last_updated_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."ResearchQuestionScore"
    ADD CONSTRAINT "ResearchQuestionScore_last_updated_by_id_fkey" FOREIGN KEY (last_updated_by_id) REFERENCES public."User"(user_id);


--
-- Name: ResearchQuestionScore ResearchQuestionScore_research_question_mapping_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."ResearchQuestionScore"
    ADD CONSTRAINT "ResearchQuestionScore_research_question_mapping_id_fkey" FOREIGN KEY (research_question_mapping_id) REFERENCES public."ResearchQuestionMapping"(research_question_mapping_id) ON DELETE CASCADE;


--
-- Name: SearchKeyword SearchKeyword_keyword_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."SearchKeyword"
    ADD CONSTRAINT "SearchKeyword_keyword_id_fkey" FOREIGN KEY (keyword_id) REFERENCES public."Keyword"(keyword_id);


--
-- Name: SearchKeyword SearchKeyword_search_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."SearchKeyword"
    ADD CONSTRAINT "SearchKeyword_search_id_fkey" FOREIGN KEY (search_id) REFERENCES public."Search"(search_id);


--
-- Name: SearchShare SearchShare_search_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."SearchShare"
    ADD CONSTRAINT "SearchShare_search_id_fkey" FOREIGN KEY (search_id) REFERENCES public."Search"(search_id);


--
-- Name: SearchShare SearchShare_shared_by_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."SearchShare"
    ADD CONSTRAINT "SearchShare_shared_by_user_id_fkey" FOREIGN KEY (shared_by_user_id) REFERENCES public."User"(user_id);


--
-- Name: SearchShare SearchShare_shared_with_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."SearchShare"
    ADD CONSTRAINT "SearchShare_shared_with_user_id_fkey" FOREIGN KEY (shared_with_user_id) REFERENCES public."User"(user_id);


--
-- Name: Search Search_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."Search"
    ADD CONSTRAINT "Search_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."User"(user_id);


--
-- Name: UserData UserData_article_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."UserData"
    ADD CONSTRAINT "UserData_article_id_fkey" FOREIGN KEY (article_id) REFERENCES public."Article"(article_id);


--
-- Name: UserData UserData_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."UserData"
    ADD CONSTRAINT "UserData_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."User"(user_id);


--
-- Name: User User_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: student
--

ALTER TABLE ONLY public."User"
    ADD CONSTRAINT "User_role_id_fkey" FOREIGN KEY (role_id) REFERENCES public."Role"(role_id);


--
-- PostgreSQL database dump complete
--

