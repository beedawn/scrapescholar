--
-- PostgreSQL database dump
--

-- Dumped from database version 14.11 (Homebrew)
-- Dumped by pg_dump version 14.11 (Homebrew)

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
105	example_keyword
106	example_keyword
107	keyword1
108	keyword2
109	keyword3
110	updated_keyword
14	example_keyword
15	example_keyword
16	keyword1
17	keyword2
18	keyword3
19	updated_keyword
235	example_keyword
236	example_keyword
237	keyword1
238	keyword2
239	keyword3
240	updated_keyword
27	example_keyword
28	example_keyword
29	keyword1
30	keyword2
31	keyword3
32	updated_keyword
118	example_keyword
119	example_keyword
120	keyword1
121	keyword2
122	keyword3
123	updated_keyword
40	example_keyword
41	example_keyword
42	keyword1
43	keyword2
44	keyword3
45	updated_keyword
53	example_keyword
54	example_keyword
55	keyword1
56	keyword2
57	keyword3
58	updated_keyword
131	example_keyword
132	example_keyword
133	keyword1
134	keyword2
135	keyword3
136	updated_keyword
66	example_keyword
67	example_keyword
68	keyword1
69	keyword2
70	keyword3
71	updated_keyword
248	example_keyword
249	example_keyword
250	keyword1
251	keyword2
252	keyword3
253	updated_keyword
79	example_keyword
80	example_keyword
81	keyword1
82	keyword2
83	keyword3
84	updated_keyword
144	example_keyword
145	example_keyword
146	keyword1
147	keyword2
148	keyword3
149	updated_keyword
92	example_keyword
93	example_keyword
94	keyword1
95	keyword2
96	keyword3
97	updated_keyword
157	example_keyword
158	example_keyword
159	keyword1
160	keyword2
161	keyword3
162	updated_keyword
261	example_keyword
262	example_keyword
263	keyword1
264	keyword2
265	keyword3
266	updated_keyword
170	example_keyword
171	example_keyword
172	keyword1
173	keyword2
174	keyword3
175	updated_keyword
183	example_keyword
184	example_keyword
185	keyword1
186	keyword2
187	keyword3
188	updated_keyword
274	example_keyword
275	example_keyword
276	keyword1
277	keyword2
278	keyword3
279	updated_keyword
196	example_keyword
197	example_keyword
198	keyword1
199	keyword2
200	keyword3
201	updated_keyword
209	example_keyword
210	example_keyword
211	keyword1
212	keyword2
213	keyword3
214	updated_keyword
287	example_keyword
288	example_keyword
289	keyword1
290	keyword2
291	keyword3
292	updated_keyword
222	example_keyword
223	example_keyword
224	keyword1
225	keyword2
226	keyword3
227	updated_keyword
300	example_keyword
301	example_keyword
302	keyword1
303	keyword2
304	keyword3
305	updated_keyword
313	example_keyword
314	example_keyword
315	keyword1
316	keyword2
317	keyword3
318	updated_keyword
326	example_keyword
327	example_keyword
328	keyword1
329	keyword2
330	keyword3
331	updated_keyword
339	example_keyword
340	example_keyword
341	keyword1
342	keyword2
343	keyword3
344	updated_keyword
391	example_keyword
394	keyword2
395	keyword3
392	example_keyword
396	updated_keyword
393	keyword1
352	example_keyword
353	example_keyword
354	keyword1
355	keyword2
356	keyword3
357	updated_keyword
365	example_keyword
366	example_keyword
367	keyword1
368	keyword2
369	keyword3
370	updated_keyword
378	example_keyword
379	example_keyword
380	keyword1
381	keyword2
382	keyword3
383	updated_keyword
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
6	PHD_Student_20241110133253412966
7	PHD_Student_20241110133253418896
8	User_20241110133253422571
9	Adjunct_Professor_20241110133253422578
10	Project_Manager_20241110133253422580
11	Updated_Role_20241110133253430753
13	PHD_Student_20241110133415483515
14	PHD_Student_20241110133415490987
15	User_20241110133415496133
16	Adjunct_Professor_20241110133415496141
17	Project_Manager_20241110133415496144
18	Updated_Role_20241110133415506741
20	PHD_Student_20241110133853847114
21	PHD_Student_20241110133853852358
22	User_20241110133853856714
23	Adjunct_Professor_20241110133853856722
24	Project_Manager_20241110133853856725
25	Updated_Role_20241110133853863926
27	PHD_Student_20241110134010823633
28	PHD_Student_20241110134010829371
29	User_20241110134010834363
30	Adjunct_Professor_20241110134010834371
31	Project_Manager_20241110134010834375
32	Updated_Role_20241110134010845885
34	PHD_Student_20241110134147183942
35	PHD_Student_20241110134147189524
36	User_20241110134147194824
37	Adjunct_Professor_20241110134147194832
38	Project_Manager_20241110134147194835
39	Updated_Role_20241110134147206141
41	PHD_Student_20241110134315460241
42	PHD_Student_20241110134315465201
43	User_20241110134315469809
44	Adjunct_Professor_20241110134315469817
45	Project_Manager_20241110134315469820
46	Updated_Role_20241110134315478786
48	PHD_Student_20241110134557975085
49	PHD_Student_20241110134557980021
50	User_20241110134557983764
51	Adjunct_Professor_20241110134557983770
52	Project_Manager_20241110134557983773
53	Updated_Role_20241110134557992843
55	PHD_Student_20241110134914406403
56	PHD_Student_20241110134914412360
57	User_20241110134914417373
58	Adjunct_Professor_20241110134914417381
59	Project_Manager_20241110134914417384
60	Updated_Role_20241110134914426338
62	PHD_Student_20241110135102055969
63	PHD_Student_20241110135102061801
64	User_20241110135102065805
65	Adjunct_Professor_20241110135102065811
66	Project_Manager_20241110135102065818
67	Updated_Role_20241110135102076527
69	PHD_Student_20241110135245612575
70	PHD_Student_20241110135245618267
71	User_20241110135245622315
72	Adjunct_Professor_20241110135245622325
73	Project_Manager_20241110135245622328
74	Updated_Role_20241110135245630141
76	PHD_Student_20241110135541932254
77	PHD_Student_20241110135541938449
78	User_20241110135541943666
79	Adjunct_Professor_20241110135541943674
80	Project_Manager_20241110135541943677
81	Updated_Role_20241110135541952768
83	PHD_Student_20241110140532066662
84	PHD_Student_20241110140532072568
85	User_20241110140532076634
86	Adjunct_Professor_20241110140532076647
87	Project_Manager_20241110140532076650
88	Updated_Role_20241110140532085270
90	PHD_Student_20241110140712188881
91	PHD_Student_20241110140712195102
92	User_20241110140712200260
93	Adjunct_Professor_20241110140712200271
94	Project_Manager_20241110140712200274
95	Updated_Role_20241110140712209828
97	PHD_Student_20241110141416571743
98	PHD_Student_20241110141416576542
99	User_20241110141416580927
100	Adjunct_Professor_20241110141416580935
101	Project_Manager_20241110141416580938
102	Updated_Role_20241110141416589588
104	PHD_Student_20241110142923866454
105	PHD_Student_20241110142923872409
106	User_20241110142923876803
107	Adjunct_Professor_20241110142923876810
108	Project_Manager_20241110142923876814
109	Updated_Role_20241110142923886240
111	PHD_Student_20241110144942472729
112	PHD_Student_20241110144942480376
113	User_20241110144942485308
114	Adjunct_Professor_20241110144942485317
115	Project_Manager_20241110144942485320
116	Updated_Role_20241110144942496618
118	PHD_Student_20241110151702419083
119	PHD_Student_20241110151702424537
120	User_20241110151702428518
121	Adjunct_Professor_20241110151702428526
122	Project_Manager_20241110151702428529
123	Updated_Role_20241110151702436471
125	PHD_Student_20241110152520312750
126	PHD_Student_20241110152520320620
127	User_20241110152520325434
128	Adjunct_Professor_20241110152520325441
129	Project_Manager_20241110152520325445
130	Updated_Role_20241110152520335878
132	PHD_Student_20241110153528093527
133	PHD_Student_20241110153528100369
134	User_20241110153528106016
135	Adjunct_Professor_20241110153528106025
136	Project_Manager_20241110153528106029
137	Updated_Role_20241110153528119248
139	PHD_Student_20241110154507050624
140	PHD_Student_20241110154507056980
141	User_20241110154507062594
142	Adjunct_Professor_20241110154507062603
143	Project_Manager_20241110154507062607
144	Updated_Role_20241110154507074408
146	PHD_Student_20241110154834155810
147	PHD_Student_20241110154834161413
148	User_20241110154834165721
149	Adjunct_Professor_20241110154834165728
150	Project_Manager_20241110154834165731
151	Updated_Role_20241110154834176225
153	PHD_Student_20241110160315234239
154	PHD_Student_20241110160315239626
155	User_20241110160315243639
156	Adjunct_Professor_20241110160315243647
157	Project_Manager_20241110160315243650
158	Updated_Role_20241110160315252021
160	PHD_Student_20241110160651438350
161	PHD_Student_20241110160651443069
162	User_20241110160651448312
163	Adjunct_Professor_20241110160651448318
164	Project_Manager_20241110160651448321
165	Updated_Role_20241110160651457494
167	PHD_Student_20241110163539742045
168	PHD_Student_20241110163539749259
169	User_20241110163539754480
170	Adjunct_Professor_20241110163539754488
171	Project_Manager_20241110163539754491
172	Updated_Role_20241110163539764944
174	PHD_Student_20241110180821141542
175	PHD_Student_20241110180821148344
176	User_20241110180821153879
177	Adjunct_Professor_20241110180821153894
178	Project_Manager_20241110180821153898
179	Updated_Role_20241110180821166928
181	PHD_Student_20241111090546196214
182	PHD_Student_20241111090546201903
183	User_20241111090546207197
184	Adjunct_Professor_20241111090546207205
185	Project_Manager_20241111090546207208
186	Updated_Role_20241111090546219268
188	PHD_Student_20241111090803768266
189	PHD_Student_20241111090803774743
190	User_20241111090803779433
191	Adjunct_Professor_20241111090803779441
192	Project_Manager_20241111090803779443
193	Updated_Role_20241111090803788609
195	PHD_Student_20241111091034698503
196	PHD_Student_20241111091034703349
197	User_20241111091034707528
198	Adjunct_Professor_20241111091034707537
199	Project_Manager_20241111091034707540
200	Updated_Role_20241111091034715924
202	PHD_Student_20241111091928737643
203	PHD_Student_20241111091928743319
204	User_20241111091928747846
205	Adjunct_Professor_20241111091928747855
206	Project_Manager_20241111091928747859
207	Updated_Role_20241111091928758961
209	PHD_Student_20241111092313519744
210	PHD_Student_20241111092313525133
211	User_20241111092313529790
212	Adjunct_Professor_20241111092313529797
213	Project_Manager_20241111092313529801
214	Updated_Role_20241111092313541405
216	PHD_Student_20241111093018976071
217	PHD_Student_20241111093018981676
218	User_20241111093018985447
219	Adjunct_Professor_20241111093018985454
220	Project_Manager_20241111093018985458
221	Updated_Role_20241111093018996150
\.


--
-- Data for Name: Search; Type: TABLE DATA; Schema: public; Owner: student
--

COPY public."Search" (search_id, user_id, search_date, search_keywords, status, title) FROM stdin;
73	1	\N	{test}	active	testuser-2024-11-11 09:09:46.274391
74	1	\N	{test}	active	testuser-2024-11-11 09:10:11.588107
141	\N	\N	{test}	active	t2_student-2024-11-11 09:22:18.149389
15	1	\N	{test}	active	testuser-2024-11-10 18:25:14.737591
16	1	\N	{test}	active	testuser-2024-11-10 18:25:49.844209
102	1	\N	{test}	active	testuser-2024-11-11 09:11:40.924141
103	1	\N	{test}	active	testuser-2024-11-11 09:13:24.724715
105	1	\N	{test}	active	testuser-2024-11-11 09:15:16.511780
107	1	\N	{test}	active	testuser-2024-11-11 09:17:08.139649
44	1	\N	{test}	active	testuser-2024-11-11 09:07:08.569584
172	\N	\N	{test}	active	t2_student-2024-11-11 09:26:05.747503
173	\N	\N	{test}	active	t2_student-2024-11-11 09:27:23.180427
176	1	\N	{test}	active	testuser-2024-11-11 09:29:38.935259
175	\N	\N	{test}	active	t2_student-2024-11-11 09:28:41.989394
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
1	gAAAAABnMPxJiITIFdhRvsQGK3pHXQqdI2M9TvZfYTe0Zj0rewm55aNOK8zaqvRHpzb7aZxCW2tILqIT8PZEiJOSvsD8dvXyNg==	$2b$12$8gmMyAlnG3EPCOTb28jAyeI3oT5ESvoWbqtD/6i/kOLTWRroWBYN2	1	$2b$12$gzGsfuzo0vynYa9gIbyKaeIU.yF9vS5FBBnwK0OSzIu3BWv2kYk1W	2024-11-10 18:32:41.936732
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

SELECT pg_catalog.setval('public."Article_article_id_seq"', 1822, true);


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

SELECT pg_catalog.setval('public."Keyword_keyword_id_seq"', 403, true);


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

SELECT pg_catalog.setval('public."Role_role_id_seq"', 222, true);


--
-- Name: SearchKeyword_search_keyword_id_seq; Type: SEQUENCE SET; Schema: public; Owner: student
--

SELECT pg_catalog.setval('public."SearchKeyword_search_keyword_id_seq"', 36, true);


--
-- Name: SearchShare_share_id_seq; Type: SEQUENCE SET; Schema: public; Owner: student
--

SELECT pg_catalog.setval('public."SearchShare_share_id_seq"', 43, true);


--
-- Name: Search_search_id_seq; Type: SEQUENCE SET; Schema: public; Owner: student
--

SELECT pg_catalog.setval('public."Search_search_id_seq"', 204, true);


--
-- Name: Source_source_id_seq; Type: SEQUENCE SET; Schema: public; Owner: student
--

SELECT pg_catalog.setval('public."Source_source_id_seq"', 313, true);


--
-- Name: UserData_userdata_id_seq; Type: SEQUENCE SET; Schema: public; Owner: student
--

SELECT pg_catalog.setval('public."UserData_userdata_id_seq"', 1744, true);


--
-- Name: User_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: student
--

SELECT pg_catalog.setval('public."User_user_id_seq"', 460, true);


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

