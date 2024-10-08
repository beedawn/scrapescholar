-- Create Role Table
CREATE TABLE "Role" (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) UNIQUE NOT NULL
);
COMMENT ON COLUMN "Role".role_name IS 'Name of the user role (e.g., Professor, Graduate Student, Undergraduate Student)';

-- Create User Table
CREATE TABLE "User" (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role_id INT REFERENCES "Role"(role_id),
    email VARCHAR(100) UNIQUE,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "User".username IS 'Unique username for each user';
COMMENT ON COLUMN "User".password IS 'Password for user authentication';
COMMENT ON COLUMN "User".role_id IS 'Foreign key referencing user role';
COMMENT ON COLUMN "User".email IS 'User email for communication and notifications';
COMMENT ON COLUMN "User".registration_date IS 'Date and time when the user registered';

-- Create Keyword Table
CREATE TABLE "Keyword" (
    keyword_id SERIAL PRIMARY KEY,
    keyword VARCHAR(255) NOT NULL
);
COMMENT ON COLUMN "Keyword".keyword IS 'Keyword used for search queries';

-- Create Source Table
CREATE TABLE "Source" (
    source_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    api_endpoint VARCHAR(255),
    scrape_source_url VARCHAR(255)
);
COMMENT ON COLUMN "Source".name IS 'Name of the source (e.g., Scopus, PubMed)';
COMMENT ON COLUMN "Source".api_endpoint IS 'API endpoint for fetching data from the source';
COMMENT ON COLUMN "Source".scrape_source_url IS 'URL for scraping data from the source';

-- Create Search Table
CREATE TABLE "Search" (
    search_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES "User"(user_id),
    search_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    search_keywords VARCHAR(255)[],
    status VARCHAR(20) DEFAULT 'active'
);
COMMENT ON COLUMN "Search".user_id IS 'Foreign key referencing the user who performed the search';
COMMENT ON COLUMN "Search".search_date IS 'Date and time when the search was conducted';
COMMENT ON COLUMN "Search".search_keywords IS 'Array of keywords used in the search';
COMMENT ON COLUMN "Search".status IS 'Status of the search (e.g., active, completed)';

-- Create Article Table
CREATE TABLE "Article" (
    article_id SERIAL PRIMARY KEY,  -- Unique identifier for each article
    source_id INT REFERENCES "Source"(source_id),  -- Foreign key referencing the source of the article
    search_id INT REFERENCES "Search"(search_id),  -- Foreign key referencing the search that retrieved this article
    title VARCHAR(255) NOT NULL,  -- Title of the article
    author VARCHAR(100),  -- Author of the article
    publication_date DATE,  -- Date when the article was published
    journal VARCHAR(100),  -- Journal where the article was published
    url VARCHAR(255),  -- URL link to the article
    relevance_score FLOAT,  -- Relevance score assigned to the article based on user evaluation
    review_status VARCHAR(20) CHECK (review_status IN ('green', 'yellow', 'red')),  -- Status indicating the relevance of the article
    abstract TEXT,  -- Abstract of the article, providing a brief summary
    doi VARCHAR(100)  -- Digital Object Identifier (DOI) for the article, optional field
);

-- Add comments for clarity on each column
COMMENT ON COLUMN "Article".source_id IS 'Foreign key referencing the source of the article';
COMMENT ON COLUMN "Article".search_id IS 'Foreign key referencing the search that retrieved this article';
COMMENT ON COLUMN "Article".title IS 'Title of the article';
COMMENT ON COLUMN "Article".author IS 'Author of the article';
COMMENT ON COLUMN "Article".publication_date IS 'Date when the article was published';
COMMENT ON COLUMN "Article".journal IS 'Journal where the article was published';
COMMENT ON COLUMN "Article".url IS 'URL link to the article';
COMMENT ON COLUMN "Article".relevance_score IS 'Relevance score assigned to the article based on user evaluation';
COMMENT ON COLUMN "Article".review_status IS 'Status indicating the relevance of the article (green, yellow, red)';
COMMENT ON COLUMN "Article".abstract IS 'Abstract of the article, providing a brief summary';
COMMENT ON COLUMN "Article".doi IS 'Digital Object Identifier (DOI) for the article, optional field';

-- Create Comment Table
CREATE TABLE "Comment" (
    comment_id SERIAL PRIMARY KEY,
    article_id INT REFERENCES "Article"(article_id),
    user_id INT REFERENCES "User"(user_id),
    comment_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "Comment".article_id IS 'Foreign key referencing the article being commented on';
COMMENT ON COLUMN "Comment".user_id IS 'Foreign key referencing the user who made the comment';
COMMENT ON COLUMN "Comment".comment_text IS 'Text content of the user comment';
COMMENT ON COLUMN "Comment".created_at IS 'Date and time when the comment was created';

-- Create Collaboration Table
CREATE TABLE "Collaboration" (
    collaboration_id SERIAL PRIMARY KEY,
    article_id INT REFERENCES "Article"(article_id),
    user_id INT REFERENCES "User"(user_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "Collaboration".article_id IS 'Foreign key referencing the article being collaborated on';
COMMENT ON COLUMN "Collaboration".user_id IS 'Foreign key referencing the user involved in the collaboration';
COMMENT ON COLUMN "Collaboration".created_at IS 'Date and time when the collaboration entry was created';

-- Create ArticleScore Table
CREATE TABLE "ArticleScore" (
    article_score_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES "User"(user_id),
    article_id INT REFERENCES "Article"(article_id),
    search_id INT REFERENCES "Search"(search_id),
    score FLOAT NOT NULL,
    last_updated_by_user_id INT REFERENCES "User"(user_id),
    evaluation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "ArticleScore".user_id IS 'Foreign key referencing the user who scored the article';
COMMENT ON COLUMN "ArticleScore".article_id IS 'Foreign key referencing the article being scored';
COMMENT ON COLUMN "ArticleScore".search_id IS 'Foreign key referencing the search associated with the score';
COMMENT ON COLUMN "ArticleScore".score IS 'Score given to the article by the user for the specific search';
COMMENT ON COLUMN "ArticleScore".last_updated_by_user_id IS 'Foreign key referencing the user who last updated the score';
COMMENT ON COLUMN "ArticleScore".evaluation_date IS 'Date and time when the score was given';
COMMENT ON COLUMN "ArticleScore".last_updated_at IS 'Date and time when the score was last updated';

-- Create SearchShare Table
CREATE TABLE "SearchShare" (
    share_id SERIAL PRIMARY KEY,
    search_id INT REFERENCES "Search"(search_id),
    shared_with_user_id INT REFERENCES "User"(user_id),
    shared_by_user_id INT REFERENCES "User"(user_id),
    share_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "SearchShare".search_id IS 'Foreign key referencing the search being shared';
COMMENT ON COLUMN "SearchShare".shared_with_user_id IS 'Foreign key referencing the user with whom the search is shared';
COMMENT ON COLUMN "SearchShare".shared_by_user_id IS 'Foreign key referencing the user who shares the search';
COMMENT ON COLUMN "SearchShare".share_date IS 'Date and time when the search was shared';

-- Create SearchKeyword Table (Junction Table)
CREATE TABLE "SearchKeyword" (
    search_keyword_id SERIAL PRIMARY KEY,
    search_id INT REFERENCES "Search"(search_id) ON DELETE CASCADE,
    keyword_id INT REFERENCES "Keyword"(keyword_id) ON DELETE CASCADE
);
COMMENT ON COLUMN "SearchKeyword".search_id IS 'Foreign key referencing the search';
COMMENT ON COLUMN "SearchKeyword".keyword_id IS 'Foreign key referencing the keyword';

-- Create the ResearchQuestion Table
CREATE TABLE "ResearchQuestion" (
    research_question_id SERIAL PRIMARY KEY,
    research_question TEXT NOT NULL
);

COMMENT ON COLUMN "ResearchQuestion".research_question_id IS 'Unique identifier for each research question';
COMMENT ON COLUMN "ResearchQuestion".research_question IS 'The text of the research question';

-- Create the ResearchQuestionMapping Table
CREATE TABLE "ResearchQuestionMapping" (
    research_question_mapping_id SERIAL PRIMARY KEY,
    article_id INTEGER NOT NULL,
    research_question_id INTEGER NOT NULL,
    FOREIGN KEY (article_id) REFERENCES "Article"(article_id) ON DELETE CASCADE,
    FOREIGN KEY (research_question_id) REFERENCES "ResearchQuestion"(research_question_id) ON DELETE CASCADE
);

COMMENT ON COLUMN "ResearchQuestionMapping".research_question_mapping_id IS 'Unique identifier for each mapping entry';
COMMENT ON COLUMN "ResearchQuestionMapping".article_id IS 'Foreign key referencing the ID of the Article table';
COMMENT ON COLUMN "ResearchQuestionMapping".research_question_id IS 'Foreign key referencing the ID of the ResearchQuestion table';

-- Create the ResearchQuestionScore Table
CREATE TABLE "ResearchQuestionScore" (
    research_Question_Score_id SERIAL PRIMARY KEY,  
    research_question_mapping_id INTEGER NOT NULL,  
    score INTEGER NOT NULL,  
    last_updated_by_id INT REFERENCES "User"(user_id),
    FOREIGN KEY (research_question_mapping_id) REFERENCES "ResearchQuestionMapping"(research_question_mapping_id) ON DELETE CASCADE
);

COMMENT ON COLUMN "ResearchQuestionScore".research_Question_Score_id IS 'Unique identifier for each score entry';
COMMENT ON COLUMN "ResearchQuestionScore".research_question_mapping_id IS 'Foreign key referencing the ID of the ResearchQuestionMapping table';
COMMENT ON COLUMN "ResearchQuestionScore".score IS 'Score value associated with the research question in an article';
COMMENT ON COLUMN "ResearchQuestionScore".last_updated_by_id IS 'The user who last updated the score (optional for tracking purposes)';
