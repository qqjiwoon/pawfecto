CREATE TABLE style_tag (
  id INT NOT NULL AUTO_INCREMENT,
  code VARCHAR(50) NOT NULL UNIQUE,
  name VARCHAR(50) NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE accounts_user (
  id INT NOT NULL AUTO_INCREMENT,
  password VARCHAR(128) NOT NULL,
  username VARCHAR(150) NOT NULL UNIQUE,
  email VARCHAR(100) NOT NULL UNIQUE,
  account_type ENUM('brand', 'creator') NOT NULL,
  name VARCHAR(255) NOT NULL,
  phone_number VARCHAR(20),
  profile_image VARCHAR(255),
  profile_image_url VARCHAR(1000),
  pet_type ENUM('dog', 'cat') NULL,
  address TEXT,
  sns_handle VARCHAR(50),
  sns_url VARCHAR(255),
  instagram_id VARCHAR(50) UNIQUE,
  total_post_count INT,
  follower_count INT,
  following_count INT,
  date_joined DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  last_login DATETIME,
  is_active BOOLEAN DEFAULT TRUE,
  is_staff BOOLEAN DEFAULT FALSE,
  is_superuser BOOLEAN DEFAULT FALSE,
  PRIMARY KEY (id)
);

CREATE TABLE user_style_tag (
  id INT NOT NULL AUTO_INCREMENT,
  user_id INT NOT NULL,
  style_tag_id INT NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (user_id) REFERENCES accounts_user(id) ON DELETE CASCADE,
  FOREIGN KEY (style_tag_id) REFERENCES style_tag(id) ON DELETE CASCADE,
  UNIQUE (user_id, style_tag_id)
);

CREATE TABLE campaign (
  campaign_id INT NOT NULL AUTO_INCREMENT,
  brand_id INT NOT NULL,
  product_name VARCHAR(100) NOT NULL,
  product_image_url VARCHAR(1000),
  product_description TEXT NOT NULL,
  target_pet_type ENUM('dog', 'cat'),
  min_follower_count INT DEFAULT 0,
  requested_at DATETIME NOT NULL,
  application_deadline_at DATE NOT NULL,
  posting_start_at DATE NOT NULL,
  posting_end_at DATE NOT NULL,
  required_creator_count INT NOT NULL,
  PRIMARY KEY (campaign_id),
  FOREIGN KEY (brand_id) REFERENCES accounts_user(id) ON DELETE CASCADE
);

CREATE TABLE campaign_style_tag (
  id INT NOT NULL AUTO_INCREMENT,
  campaign_id INT NOT NULL,
  style_tag_id INT NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (campaign_id) REFERENCES campaign(campaign_id) ON DELETE CASCADE,
  FOREIGN KEY (style_tag_id) REFERENCES style_tag(id) ON DELETE CASCADE,
  UNIQUE (campaign_id, style_tag_id)
);

CREATE TABLE campaign_acceptance (
  campaign_acceptance_id INT NOT NULL AUTO_INCREMENT,
  creator_id INT NOT NULL,
  campaign_id INT NOT NULL,
  brand_decision_status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
  brand_decided_at DATETIME,
  acceptance_status ENUM('pending', 'accepted', 'rejected', 'completed') DEFAULT 'pending',
  applied_at DATETIME,
  accepted_at DATETIME,
  PRIMARY KEY (campaign_acceptance_id),
  FOREIGN KEY (creator_id) REFERENCES accounts_user(id) ON DELETE CASCADE,
  FOREIGN KEY (campaign_id) REFERENCES campaign(campaign_id) ON DELETE CASCADE,
  UNIQUE (campaign_id, creator_id)
);

CREATE TABLE deliverable_requirement (
  id INT NOT NULL AUTO_INCREMENT,
  campaign_id INT NOT NULL,
  requirement_type ENUM('object', 'scene', 'action', 'text') NOT NULL,
  description VARCHAR(255) NOT NULL,
  is_required BOOLEAN DEFAULT TRUE,
  PRIMARY KEY (id),
  FOREIGN KEY (campaign_id) REFERENCES campaign(campaign_id) ON DELETE CASCADE
);

CREATE TABLE deliverable (
  deliverable_id INT NOT NULL AUTO_INCREMENT,
  campaign_acceptance_id INT NOT NULL UNIQUE,
  content TEXT,
  image VARCHAR(255),
  post_url VARCHAR(255),
  posted_at DATETIME,
  deliverable_status ENUM('incomplete', 'completed') DEFAULT 'incomplete',
  ai_validation_status ENUM('pending', 'passed', 'failed') DEFAULT 'pending',
  ai_result_raw JSON,
  submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (deliverable_id),
  FOREIGN KEY (campaign_acceptance_id) REFERENCES campaign_acceptance(campaign_acceptance_id) ON DELETE CASCADE
);