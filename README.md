<div id="top">

<!-- HEADER STYLE: ASCII -->
<div align="center">
<pre>
 ████   ████  ██   ██ ██   ██ ██████  ████  ██████ ██     ██  ██ 
██     ██  ██ ███  ██ ███  ██ ██     ██       ██   ██      ████  
██     ██  ██ ██ █ ██ ██ █ ██ ████   ██       ██   ██       ██   
██     ██  ██ ██  ███ ██  ███ ██     ██       ██   ██       ██   
 ████   ████  ██   ██ ██   ██ ██████  ████    ██   ██████   ██   
</pre>
</div>
<div align="center">

<em></em>

<!-- BADGES -->
<!-- local repository, no metadata badges. -->

<em>Built with the tools and technologies:</em>

<img src="https://img.shields.io/badge/Django-092E20.svg?style=flat-square&logo=Django&logoColor=white" alt="Django">
<img src="https://img.shields.io/badge/Pytest-0A9EDC.svg?style=flat-square&logo=Pytest&logoColor=white" alt="Pytest">
<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat-square&logo=Python&logoColor=white" alt="Python">

</div>
<br>

## 📄 Table of Contents

<details>
<summary>Table of Contents</summary>

- [📄 Table of Contents](#-table-of-contents)
- [✨ Overview](#-overview)
- [📌 Features](#-features)
- [📁 Project Structure](#-project-structure)
	- [📑 Project Index](#-project-index)
- [🚀 Getting Started](#-getting-started)
	- [📋 Prerequisites](#-prerequisites)
	- [⚙️ Installation](#️-installation)
	- [💻 Usage](#-usage)
		- [User Endpoints](#user-endpoints)
		- [Post Endpoints](#post-endpoints)
		- [Comment Endpoints](#comment-endpoints)
		- [Profile Endpoints](#profile-endpoints)
	- [📲 API](#-api)
	- [🧪 Testing](#-testing)
- [✨ Acknowledgments](#-acknowledgments)

</details>

---

## ✨ Overview
Connectly is a Django-based social media platform that enables users to create profiles, share posts, interact with content, and connect with others. 
The platform provides a robust API for user management, content creation, and social interactions.

Key aspects of Connectly include:

- Secure user authentication with Google OAuth2 and JWT tokens

- Content management system for posts and comments with media support

- Social features including following users and liking content

- Role-based access control for administrators and moderators

- Comprehensive testing suite with pytest

- Scalable architecture with middleware for pagination and rate limiting

The platform is designed to be developer-friendly with clear API endpoints, thorough documentation, and modular structure for easy maintenance and extension.


---

## 📌 Features

| Component                    | Details                              |
|:-----------------------------| :----------------------------------- |
| **User Management**          | <ul><br/><li>User registration and profile creation</li><li>Google OAuth2 authentication</li><li>JWT token-based authentication</li><li>Role-based permissions (Admin, Moderator)</li><li>Profile customization (bio, personal info)</li></ul>|
| **Content System**           | <ul><li>Create, read, update, and delete posts</li><li>Post comments with nested replies</li><li>Media attachments (images and videos)</li><li>Automatic media compression</li><li>Privacy settings for posts</li></ul>                                     |
| **Social Features**          | <ul><li>Follow/unfollow other users</li><li>Like/unlike posts and comments</li><li>View user feeds</li><li>Profile browsing and search</li></ul>                                     |
| **Technical Infrastructure** | <ul><li>Rate limiting middleware</li><li>Pagination support</li><li>Centralized logging</li><li>Configuration management</li><li>Standardized response formatting</li></ul>                                     |
| **Development Tools**        | <ul><li>Comprehensive test suite</li><li>Factory-based test data generation</li><li>API documentation</li><li>SQLite database (development)</li><li>Django admin interface</li></ul>                                    |
---
The features are implemented with a focus on performance, security, and maintainability, following Django best practices and REST API design principles.

## 📁 Project Structure

```sh
└── Connectly/
    ├── apps
    │   ├── medias
    │   ├── posts
    │   └── users
    ├── connectly
    │   ├── middleware
    │   ├── settings.py
    │   ├── urls.py
    │   ├── views.py
    │   └── wsgi.py
    ├── db.sqlite3
    ├── manage.py
    ├── media
    │   ├── comment_images
    │   ├── post_images
    │   └── post_videos
    ├── pytest.ini
    ├── README.md
    ├── requirements.txt
    ├── tests
    │   ├── utils
    │   └── views
    └── utils
        ├── config_manager.py
        ├── logger.py
        ├── media_compressor.py
        ├── rate_limiter.py
        └── response_factory.py
```

### 📑 Project Index

<details open>
	<summary><b><code>Connectly</code></b></summary>
	<!-- __root__ Submodule -->
	<details>
		<summary><b>__root__</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ __root__</b></code>
			<table style='width: 100%; border-collapse: collapse;'>
			<thead>
				<tr style='background-color: #f8f9fa;'>
					<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
					<th style='text-align: left; padding: 8px;'>Summary</th>
				</tr>
			</thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/cert.crt'>cert.crt</a></b></td>
					<td style='padding: 8px;'>- Generate Certificate Files<br>- The cert.crt file provides a self-signed certificate for testing purposes, ensuring secure communication between systems<br>- It enables the creation of trusts and secure connections without relying on external certificate authorities<br>- This certificate file is used to establish a secure connection between clients and servers in various development environments.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/db.sqlite3'>db.sqlite3</a></b></td>
					<td style='padding: 8px;'>Real-time Data AggregationIt enables efficient collection and aggregation of product data from various sources, ensuring seamless synchronization across the platform.<em> <strong>Automated Inventory updates by integrating with our existing backend infrastructure, it facilitates automated updates to inventory levels, reducing manual errors and improving overall accuracy.</em> </strong>Data-Driven Decision making the code provides a robust foundation for data analysis, enabling us to gain valuable insights into product trends, demand patterns, and supply chain efficiency.By leveraging this component, EcoSphere is poised to deliver a streamlined user experience, enhanced operational efficiency, and data-driven decision support capabilities.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/manage.py'>manage.py</a></b></td>
					<td style='padding: 8px;'>- Launches the Django development server to execute administrative tasks<br>- The manage.py script serves as a command-line utility for various Django-related operations<br>- It ensures proper setup and activation of virtual environments, setting the stage for project initialization and management<br>- With this script, users can effortlessly run administrative tasks, facilitating efficient project development and deployment.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/pytest.ini'>pytest.ini</a></b></td>
					<td style='padding: 8px;'>- Reorganizes test configurations<br>- The pytest.ini file configures Pytest to run tests in the project, utilizing the Django settings module and specifying test files with a <code>.py</code> extension<br>- It enables reporting of test results, allowing for efficient testing of connected components within the Connectly application.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/requirements.txt'>requirements.txt</a></b></td>
					<td style='padding: 8px;'>- Architecture OverviewThe <code>requirements.txt</code> file serves as the central configuration point for the projects dependencies, specifying a comprehensive set of packages to ensure seamless integration and execution across the entire codebase architecture<br>- It enables smooth collaboration and versioning management, ultimately supporting the efficient development, testing, and deployment of the Django-based application.</td>
				</tr>
			</table>
		</blockquote>
	</details>
	<!-- apps Submodule -->
	<details>
		<summary><b>apps</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ apps</b></code>
			<!-- medias Submodule -->
			<details>
				<summary><b>medias</b></summary>
				<blockquote>
					<div class='directory-path' style='padding: 8px 0; color: #666;'>
						<code><b>⦿ apps.medias</b></code>
					<table style='width: 100%; border-collapse: collapse;'>
					<thead>
						<tr style='background-color: #f8f9fa;'>
							<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
							<th style='text-align: left; padding: 8px;'>Summary</th>
						</tr>
					</thead>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/apps\medias\admin.py'>admin.py</a></b></td>
							<td style='padding: 8px;'>- Simplifies media administration by registering models with the Django admin interface.The <code>admin.py</code> file plays a crucial role in setting up media management capabilities within the project, enabling administrators to efficiently manage and interact with media-related data<br>- By registering models here, you enable the admin interface to display and edit media content according to your projects structure and requirements.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/apps\medias\apps.py'>apps.py</a></b></td>
							<td style='padding: 8px;'>- Configures Django Application**MediasConfig enables a Django application with database configuration and naming conventions<br>- It sets the default auto-field to BigAutoField and defines the applications namespace as apps.medias<br>- This configuration provides a solid foundation for building media-related features within the Django application, aligning with the broader project structure.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/apps\medias\factories.py'>factories.py</a></b></td>
							<td style='padding: 8px;'>- The media factory class in <code>apps.medias.factories.py</code> creates and manages different types of media files associated with content objects, such as images and videos<br>- It provides a standardized way to create and save media files, ensuring consistency across the project<br>- By leveraging Djangos built-in models and content types, it streamlines media file creation and upload processes.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/apps\medias\models.py'>models.py</a></b></td>
							<td style='padding: 8px;'>- Model Definition Purpose**Defines a <code>Media</code> model that stores files with corresponding metadata, automatically generating unique file names and timestamps<br>- The model supports image and video types, with optional JSON metadata fields and a foreign key referencing the content type of associated objects<br>- This design enables flexible storage and retrieval of media assets within the applications architecture.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/apps\medias\serializers.py'>serializers.py</a></b></td>
							<td style='padding: 8px;'>- The <code>serializers.py</code> file provides a serializer class for the <code>Media</code> model, enabling data exchange between the models and external applications<br>- It determines the valid media types and compresses files accordingly, while maintaining metadata integrity<br>- This serialization process ensures consistent and efficient data transfer within the projects architecture.</td>
						</tr>
					</table>
					<!-- migrations Submodule -->
					<details>
						<summary><b>migrations</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ apps.medias.migrations</b></code>
							<table style='width: 100%; border-collapse: collapse;'>
							<thead>
								<tr style='background-color: #f8f9fa;'>
									<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
									<th style='text-align: left; padding: 8px;'>Summary</th>
								</tr>
							</thead>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/apps\medias\migrations\0001_initial.py'>0001_initial.py</a></b></td>
									<td style='padding: 8px;'>- The <code>0001_initial.py</code> migration file sets up the initial database schema for the media management system<br>- It creates a new <code>Media</code> model with fields to store various types of media files, such as images and videos, along with metadata and object IDs<br>- This marks the foundation of the projects data structure, providing a starting point for further development and expansion.</td>
								</tr>
							</table>
						</blockquote>
					</details>
				</blockquote>
			</details>
			<!-- posts Submodule -->
			<details>
				<summary><b>posts</b></summary>
				<blockquote>
					<div class='directory-path' style='padding: 8px 0; color: #666;'>
						<code><b>⦿ apps.posts</b></code>
					<table style='width: 100%; border-collapse: collapse;'>
					<thead>
						<tr style='background-color: #f8f9fa;'>
							<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
							<th style='text-align: left; padding: 8px;'>Summary</th>
						</tr>
					</thead>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/apps\posts\admin.py'>admin.py</a></b></td>
							<td style='padding: 8px;'>- The <code>admin.py</code> file serves as a critical entry point for configuring Djangos admin interface for posts management<br>- It enables administrators to view, create, edit, and delete post-related data in a centralized manner<br>- By registering models within this file, users can efficiently manage their content, allowing for streamlined content creation and updates.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/apps\posts\apps.py'>apps.py</a></b></td>
							<td style='padding: 8px;'>- Configures the posts application within the Django project<br>- Establishes the default auto-field type and app name, enabling the post application to function correctly<br>- Integrates with the broader project structure, allowing for seamless deployment and management of posts-related features and functionality<br>- Enables app registration and configuration for proper Django maintenance and updates.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/apps\posts\factories.py'>factories.py</a></b></td>
							<td style='padding: 8px;'>- The post factories provide a crucial foundation for the entire codebase architecture by enabling efficient creation of post and comment instances<br>- By leveraging Djangos ORM, these factories standardize the process of generating posts and comments, ensuring data consistency across the application<br>- They serve as a critical building block for populating the project with sample data, facilitating testing and development workflows.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/apps\posts\models.py'>models.py</a></b></td>
							<td style='padding: 8px;'>- Validates and restricts post and comment content creation to adhere to established guidelines<br>- The <code>clean</code> method checks for excessive media files (20 images, 1 video), while the <code>save</code> method ensures that author changes are not allowed on existing posts<br>- Similarly, it prevents changing of comments associated posts or commenters<br>- These constraints maintain data coherence and prevent misuse, ensuring a secure and organized content management system.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/apps\posts\permissions.py'>permissions.py</a></b></td>
							<td style='padding: 8px;'>- Provides fine-grained permission control for posts within the application<br>- The <code>IsAuthor</code> class restricts access to post creation and editing only for the posts author, while allowing read-only access to all users<br>- The <code>IsOwnerOrReadOnly</code> class grants read-only access to others posts if the user is not the owner, ensuring a balance between authorization and data accessibility.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/apps\posts\serializers.py'>serializers.py</a></b></td>
							<td style='padding: 8px;'>- Provides a comprehensive API serialization framework for managing comments on posts within the platforms content management system<br>- Enables efficient data exchange between front-end and back-end applications, ensuring seamless integration of comment features and media support<br>- Facilitates validation, creation, and updating of comments and associated media files.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/apps\posts\tests.py'>tests.py</a></b></td>
							<td style='padding: 8px;'>- Test Suite Enabler**The <code>tests.py</code> file enables the test suite for the post application, allowing users to create and run tests to ensure the functionality and integrity of the codebase<br>- By leveraging Djangos built-in testing framework, this module facilitates a structured approach to quality assurance, ultimately contributing to a more robust and reliable project environment.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/apps\posts\urls.py'>urls.py</a></b></td>
							<td style='padding: 8px;'>- Defines the URL patterns for a Django-based blog application, mapping URLs to view functions that handle post and comment listings, details, liking, and commenting actions<br>- The code enables users to navigate and interact with posts and comments in a structured and efficient manner, facilitating the core functionality of the application.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/apps\posts\views.py'>views.py</a></b></td>
							<td style='padding: 8px;'>- Invalid likes and dislikes are being stored multiple times due to a faulty many-to-many relationship<br>- The <code>liked_by</code> field is storing user IDs but not the associated post comment IDs<br>- This can be resolved by adding foreign key fields to the models.</td>
						</tr>
					</table>
					<!-- migrations Submodule -->
					<details>
						<summary><b>migrations</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ apps.posts.migrations</b></code>
							<table style='width: 100%; border-collapse: collapse;'>
							<thead>
								<tr style='background-color: #f8f9fa;'>
									<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
									<th style='text-align: left; padding: 8px;'>Summary</th>
								</tr>
							</thead>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/apps\posts\migrations\0001_initial.py'>0001_initial.py</a></b></td>
									<td style='padding: 8px;'>- Initialize the projects database schema<br>- The <code>0001_initial.py</code> file creates the core models for a blog application, including Post, Comment, and their respective image and video extensions, which establish relationships with user authentication and liking functionality<br>- This migration sets the foundation for the entire codebase architecture, enabling data storage and interaction between users, posts, comments, images, and videos.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/apps\posts\migrations\0002_remove_comment_image.py'>0002_remove_comment_image.py</a></b></td>
									<td style='padding: 8px;'>- Migrates Django database schema by removing the image field from the comment model, effectively reversing a previous migration step<br>- This change is part of a larger refactoring effort to improve the overall structure and maintainability of the project<br>- The removal of this field aligns with the project's goal of streamlining its functionality and promoting data consistency across different models.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/apps\posts\migrations\0003_remove_postimage_post_remove_postvideo_post_and_more.py'>0003_remove_postimage_post_remove_postvideo_post_and_more.py</a></b></td>
									<td style='padding: 8px;'>- This migration file updates the database schema by removing fields from the <code>PostImage</code> model and deleting associated models<br>- It ensures data integrity by removing references to non-existent models, enabling future schema changes without breaking existing data<br>- The migration is part of a larger project restructuring effort to improve data management and scalability.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/apps\posts\migrations\0004_alter_comment_content_alter_post_content.py'>0004_alter_comment_content_alter_post_content.py</a></b></td>
									<td style='padding: 8px;'>- Migrates Django Post Model FieldsThe provided migration script updates two model fields in the posts' application to allow blank values<br>- It aligns with the project's database schema evolution, ensuring data integrity and enabling the collection of optional post content<br>- This change enables a flexible and scalable content management system for the application.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/apps\posts\migrations\0005_post_privacy_type.py'>0005_post_privacy_type.py</a></b></td>
									<td style='padding: 8px;'>- Public, Private, and Followers<br>- It builds upon an existing migration framework, leveraging Django's built-in features<br>- The update expands the post's metadata to accommodate more granular privacy settings, enhancing data security and management capabilities within the project.</td>
								</tr>
							</table>
						</blockquote>
					</details>
				</blockquote>
			</details>
			<!-- users Submodule -->
			<details>
				<summary><b>users</b></summary>
				<blockquote>
					<div class='directory-path' style='padding: 8px 0; color: #666;'>
						<code><b>⦿ apps.users</b></code>
					<table style='width: 100%; border-collapse: collapse;'>
					<thead>
						<tr style='background-color: #f8f9fa;'>
							<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
							<th style='text-align: left; padding: 8px;'>Summary</th>
						</tr>
					</thead>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/apps\users\admin.py'>admin.py</a></b></td>
							<td style='padding: 8px;'>- Establishes the Django admin interface for user management<br>- Enables administrators to view, edit, and manage users within the system<br>- Facilitates data entry and modification of user information, ensuring a centralized and organized approach to user management<br>- Integrates with existing project structure, allowing for streamlined data access and manipulation.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/apps\users\apps.py'>apps.py</a></b></td>
							<td style='padding: 8px;'>- Initialize User Configuration**The <code>apps.py</code> file initializes the user configuration for the project, setting up the necessary configuration for Djangos built-in authentication and authorization system<br>- It enables role-based access controls by defining default auto-field settings and imports signals to create groups after applying migrations<br>- This setup ensures seamless integration with other parts of the project, ensuring secure and efficient user management.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/apps\users\authentication.py'>authentication.py</a></b></td>
							<td style='padding: 8px;'>- Validates Google OAuth2 access tokens for authentication purposes<br>- The <code>GoogleAuthentication</code> class checks the token against Googles Userinfo API to verify its validity and retrieves user data, which is then used to create or update a corresponding user in the database<br>- It integrates with Djangos authentication system and Simple JWT middleware to handle various authentication scenarios.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/apps\users\factories.py'>factories.py</a></b></td>
							<td style='padding: 8px;'>- Fabricates user profiles and handles user role assignments<br>- The UserFactory class creates users with associated profiles, checks for existing usernames and emails, and sets up roles through group associations<br>- It also provides methods to create admin users specifically<br>- The factory ensures data consistency and validation for user creation, making it a crucial component of the projects backend logic.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/apps\users\models.py'>models.py</a></b></td>
							<td style='padding: 8px;'>- Profile<code> and </code>Follow<code><br>- The </code>Profile<code> model creates a one-to-one relationship between a user and their profile information, including first name, last name, bio, and creation date<br>- Meanwhile, the </code>Follow` model establishes a many-to-many relationship for user follow relationships, ensuring that each follower is only associated with unique followed users.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/apps\users\permissions.py'>permissions.py</a></b></td>
							<td style='padding: 8px;'>- Summary**Enforces fine-grained permission control on user actions, distinguishing between Admin, Moderator, and Owner/Admin roles<br>- Validates user groups against predefined names to grant or deny access to protected routes<br>- Integrates seamlessly with the projects authentication system, ensuring secure authorization and access management for users within the <code>users</code> app.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/apps\users\serializers.py'>serializers.py</a></b></td>
							<td style='padding: 8px;'>- Generates User Data Representation**The provided serializers generate JSON representations of users, profiles, and follow relationships, enabling data exchange between the frontend and backend<br>- They validate user input, create new profiles, and handle updates to existing ones<br>- The serializers ensure data consistency and integrity across different parts of the application.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/apps\users\signals.py'>signals.py</a></b></td>
							<td style='padding: 8px;'>- Initializes Default User Groups and Admin User After Migrations**The <code>signals.py</code> file plays a crucial role in setting up the initial user groups and admin user upon migrations, ensuring a solid foundation for the project<br>- It creates default user groups (Admin and Moderator) and a default admin user with associated profile and group assignments<br>- This setup is critical for the projects core functionality and security.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/apps\users\tests.py'>tests.py</a></b></td>
							<td style='padding: 8px;'>- The <code>tests.py</code> file serves as a testing foundation for the user application, ensuring its functionality is thoroughly tested and validated<br>- It provides a robust set of tests that verify the correctness of user-related endpoints, allowing developers to confidently deploy and maintain the application<br>- By leveraging Djangos testing framework, this codebase prioritizes reliability and quality assurance.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/apps\users\urls.py'>urls.py</a></b></td>
							<td style='padding: 8px;'>- Configures URL routes for the users app, establishing connections between user data management and profile-related features<br>- Enables interaction with various views, including listing users, updating profiles, registering new accounts, changing roles, and accessing user feeds, profiles, posts, comments, and follow status<br>- Facilitates seamless navigation within the apps core functionality.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/apps\users\views.py'>views.py</a></b></td>
							<td style='padding: 8px;'>- Retrieves the profile of a specific user.<em> <strong>POSTCreates a new profile for an authenticated user.</em> </strong>PUT/{user_id}Updates an existing profile.<em> <strong>DELETE/{user_id}Deletes a profile.</strong>Comments and Posts<strong></em> </strong>GETRetrieves comments or posts from a specific user.<em> <strong>POSTCreates a new comment or post for an authenticated user.</em> </strong>PUT/{comment_id}<strong>/</strong>{post_id}Updates an existing comment or post.<em> <strong>DELETE/{comment_id}</strong>/<strong>{post_id}Deletes a comment or post.</strong>Followers and Following<strong></em> </strong>GET/{user_id}?type=following/followerRetrieves followers or following users for a specific user.<em> </em>Follows or unfollows another user.The API uses caching to improve performance by storing frequently accessed data in memory<br>- It also employs authentication and authorization mechanisms using Djangos built-in system to ensure only authorized users can modify their profiles, create comments and posts, and follow/unfollow other users.</td>
						</tr>
					</table>
					<!-- migrations Submodule -->
					<details>
						<summary><b>migrations</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ apps.users.migrations</b></code>
							<table style='width: 100%; border-collapse: collapse;'>
							<thead>
								<tr style='background-color: #f8f9fa;'>
									<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
									<th style='text-align: left; padding: 8px;'>Summary</th>
								</tr>
							</thead>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/apps\users\migrations\0001_initial.py'>0001_initial.py</a></b></td>
									<td style='padding: 8px;'>- This migration script creates the initial database schema for a user management system, including <code>Profile</code> and <code>Follow</code> models<br>- It establishes relationships between users and allows followers to follow each other while maintaining uniqueness constraints<br>- The schema provides a foundation for user profiles and friend relationships, enabling data storage and retrieval for the application.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/apps\users\migrations\0002_alter_profile_id.py'>0002_alter_profile_id.py</a></b></td>
									<td style='padding: 8px;'>- The <code>0002_alter_profile_id.py</code> migration file upgrades the database schema by altering the <code>id</code> field of the <code>Profile</code> model to use an auto-incrementing primary key<br>- This change ensures data consistency and enables efficient management of user profiles<br>- Part of a larger Django project, this migration is triggered automatically when running migrations.</td>
								</tr>
							</table>
						</blockquote>
					</details>
				</blockquote>
			</details>
		</blockquote>
	</details>
	<!-- connectly Submodule -->
	<details>
		<summary><b>connectly</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ connectly</b></code>
			<table style='width: 100%; border-collapse: collapse;'>
			<thead>
				<tr style='background-color: #f8f9fa;'>
					<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
					<th style='text-align: left; padding: 8px;'>Summary</th>
				</tr>
			</thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/connectly\asgi.py'>asgi.py</a></b></td>
					<td style='padding: 8px;'>- Configures the ASGI environment for the Connectly project<br>- Establishes a connection to Djangos settings and exposes it as an ASGI application<br>- Enabling the project to run under ASGI, allowing for efficient asynchronous request handling<br>- Facilitating deployment and integration with other frameworks in an async-friendly manner.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/connectly\settings.py'>settings.py</a></b></td>
					<td style='padding: 8px;'>- *Configures Django Environment*This settings file configures the Django environment for a Connectly project<br>- It enables authentication through Google and Simple JWT, sets up CORS headers, and defines application definitions and middleware classes<br>- The configuration also specifies database connections, caching, and security settings for the project<br>- This file serves as the backbone of the projects infrastructure, providing a solid foundation for development and deployment.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/connectly\urls.py'>urls.py</a></b></td>
					<td style='padding: 8px;'>- Configures URLs for the Connectly project, defining routes for various endpoints, including administrative dashboards, user profiles, and authentication tokens<br>- Establishes a foundation for handling incoming requests and directing them to corresponding views, ensuring seamless interaction between different aspects of the application<br>- Provides a centralized hub for URL routing and validation.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/connectly\views.py'>views.py</a></b></td>
					<td style='padding: 8px;'>- The <code>connectly/views.py</code> file implements a logout request handler that verifies the validity of a refresh token and blacklists it upon successful logout<br>- Upon successful verification, it returns a success response with a status code of 200<br>- If any errors occur during validation or token processing, an error response is returned with a relevant HTTP status code.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/connectly\wsgi.py'>wsgi.py</a></b></td>
					<td style='padding: 8px;'>- *Initialize API Framework* The <code>wsgi.py</code> file serves as the entry point for the Connectly projects web application framework, exposing the WSGI callable as a module-level variable named <code>application</code><br>- It sets up Django's environment and initializes logging<br>- By running this file, the API is made available for deployment, enabling users to access the project's features and functionality.</td>
				</tr>
			</table>
			<!-- middleware Submodule -->
			<details>
				<summary><b>middleware</b></summary>
				<blockquote>
					<div class='directory-path' style='padding: 8px 0; color: #666;'>
						<code><b>⦿ connectly.middleware</b></code>
					<table style='width: 100%; border-collapse: collapse;'>
					<thead>
						<tr style='background-color: #f8f9fa;'>
							<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
							<th style='text-align: left; padding: 8px;'>Summary</th>
						</tr>
					</thead>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/connectly\middleware\pagination_middleware.py'>pagination_middleware.py</a></b></td>
							<td style='padding: 8px;'>- The <code>pagination_middleware.py</code> file enables paginated responses for API queries, allowing users to navigate through results efficiently<br>- It leverages Djangos built-in pagination functionality with customizable page size settings<br>- This middleware ensures that response data is properly formatted and serializable for JSON output, making it easier for clients to handle pagination in their applications.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/connectly\middleware\rate_limit_middleware.py'>rate_limit_middleware.py</a></b></td>
							<td style='padding: 8px;'>- *Enforce Rate Limiting Across API Endpoints*This middleware class enforces rate limiting on API requests to prevent abuse and ensure fair usage<br>- It integrates with a memory-based rate limiter, allowing clients to reach their allowed request rates within a specified time window<br>- By implementing rate limiting, the project ensures the integrity of its API and protects it from excessive traffic.</td>
						</tr>
					</table>
				</blockquote>
			</details>
		</blockquote>
	</details>
	<!-- utils Submodule -->
	<details>
		<summary><b>utils</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ utils</b></code>
			<table style='width: 100%; border-collapse: collapse;'>
			<thead>
				<tr style='background-color: #f8f9fa;'>
					<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
					<th style='text-align: left; padding: 8px;'>Summary</th>
				</tr>
			</thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/utils\config_manager.py'>config_manager.py</a></b></td>
					<td style='padding: 8px;'>- Manages the applications configuration settings as a singleton class, providing access to default values and allowing setting updates through methods such as <code>get_settings</code> and <code>set_settings</code><br>- Ensures consistency across the project by initializing settings with a predefined set of defaults<br>- Facilitates centralized management of application configuration.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/utils\logger.py'>logger.py</a></b></td>
					<td style='padding: 8px;'>- Achieves centralized logging configuration across the application<br>- The <code>Logger</code> class ensures a single instance is created and reused throughout the project, providing a consistent logging experience with configurable output formats and levels<br>- Facilitates controlled logging behavior, allowing for easy adaptation to different environments and use cases.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/utils\media_compressor.py'>media_compressor.py</a></b></td>
					<td style='padding: 8px;'>This implements the <code>ImageAndVideoProcessing</code> class, offering functionality for compressing images and videos. The `compress_image` method handles resizing and saving images in formats like JPEG or PNG, while `compress_video` uses ffmpeg to compress video files with specified bitrates. Both methods include error handling using <code>ValidationError</code>.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/utils\rate_limiter.py'>rate_limiter.py</a></b></td>
					<td style='padding: 8px;'>- The rate limiter factory enables the creation of various rate limiters, including an in-memory rate limiter that stores request timestamps and cleans up old data regularly to maintain a specified request threshold within a given time window<br>- The factory provides a flexible way to create different types of rate limiters based on user configuration settings.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='E:\GitHub\MMDC\IntegProg\Connectly/blob/master/utils\response_factory.py'>response_factory.py</a></b></td>
					<td style='padding: 8px;'>Creates standardized HTTP responses for Django REST framework applications.Generates responses with various HTTP status codes (200 OK, 201 Created, 204 No Content, etc.) and logs messages at different levels.Facilitates uniform error handling and provides a consistent response structure across the application.</td>
				</tr>
			</table>
		</blockquote>
	</details>
</details>

---

## 🚀 Getting Started

### 📋 Prerequisites

This project requires the following dependencies:

- **Programming Language:** Python
- **Package Manager:** Pip

### ⚙️ Installation

Build Connectly from the source and intsall dependencies:

1. Clone the repository:
```
git clone https://github.com/your-username/connectly.git
```

2. Create a virtual environment and activate it:
```
python -m venv venv
source venv/bin/activate
```

3. Install the required dependencies:
```
pip install -r requirements.txt
```

4. Apply the database migrations:
```
python manage.py migrate
```

5. Start the development server:
```
python manage.py runserver
```

The API will be available at `http://localhost:8000/`.

### 💻 Usage

The Connectly API provides the following endpoints:

#### User Endpoints
- `POST /users/register/`: Register a new user.
- `PATCH /users/<int:user_id>`: Update a user's profile.
- `DELETE /users/<int:user_id>`: Delete a user.
- `POST /users/role/<int:user_id>`: Change a user's role (Admin or Moderator).

#### Post Endpoints
- `GET /posts/`: List all posts.
- `POST /posts/`: Create a new post.
- `GET /posts/<int:post_id>/`: Retrieve a specific post.
- `PATCH /posts/<int:post_id>/`: Update a post.
- `DELETE /posts/<int:post_id>/`: Delete a post.
- `POST /posts/<int:post_id>/like`: Like a post.
- `DELETE /posts/<int:post_id>/like`: Unlike a post.

#### Comment Endpoints
- `GET /posts/<int:post_id>/comments/`: List comments for a specific post.
- `POST /posts/<int:post_id>/comments/`: Create a new comment.
- `GET /posts/<int:post_id>/comments/<int:comment_id>/`: Retrieve a specific comment.
- `PUT /posts/<int:post_id>/comments/<int:comment_id>/`: Update a comment.
- `DELETE /posts/<int:post_id>/comments/<int:comment_id>/`: Delete a comment.
- `POST /posts/<int:post_id>/comments/<int:comment_id>/like`: Like a comment.
- `DELETE /posts/<int:post_id>/comments/<int:comment_id>/like`: Unlike a comment.

#### Profile Endpoints
- `GET /profiles/`: Search for user profiles.
- `GET /profiles/<str:user_id>/`: Retrieve a user's profile.
- `PATCH /profiles/<str:user_id>/`: Update a user's profile.
- `DELETE /profiles/<str:user_id>/`: Delete a user's profile.
- `GET /profiles/<str:user_id>/posts/`: Retrieve a user's posts.
- `GET /profiles/<str:user_id>/comments/`: Retrieve a user's comments.
- `POST /profiles/<str:user_id>/follow`: Follow a user.
- `DELETE /profiles/<str:user_id>/follow`: Unfollow a user.

### 📲 API

The Connectly API uses the following technologies:

- Django
- Django REST Framework
- Simple JWT for authentication
- SQLite database (for development)

The API supports the following features:

- User registration and authentication
- CRUD operations for posts and comments
- Liking and unliking posts and comments
- Searching and retrieving user profiles
- Following and unfollowing users
- Role-based access control (Admin and Moderator roles)
  

### 🧪 Testing

The project includes a comprehensive test suite built with pytest. To run the tests, execute the following command:

```
pytest
```

The test suite covers the following areas:

- User registration and authentication
- Post and comment CRUD operations
- Liking and unliking posts and comments
- Profile search and retrieval
- Following and unfollowing users
- Role-based access control

The test suite also includes fixtures for setting up the test environment and mocking external dependencies (eg., image and video processing).

---

## ✨ Acknowledgments

- Owners: [@hatudoggy](https://github.com/hatudoggy), [@Morfusee](https://github.com/Morfusee), [@IbraDoesCode](https://github.com/IbraDoesCode), [@DroidZeroCodes](https://github.com/DroidZeroCodes)

<div align="right">

[![][back-to-top]](#top)

</div>


[back-to-top]: https://img.shields.io/badge/-BACK_TO_TOP-151515?style=flat-square


---
