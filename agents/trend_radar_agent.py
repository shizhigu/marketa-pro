from google.adk import Agent, Runner
from google.adk.tools import ToolContext, FunctionTool
from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import InMemorySessionService
from typing import Dict, List, Any, Optional
import logging
import json

# Import configuration
from utils.config import get_model_config, DEFAULT_MODEL

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define model constants
MODEL_GEMINI_1_5_PRO = DEFAULT_MODEL

class TrendRadarAgent:
    """
    Agent responsible for identifying trending topics, keywords, and content directions
    for specific e-commerce platforms through web crawling and data analysis
    """
    
    def __init__(self, app_name: str = "marketa-pro"):
        """
        Initialize Trend Radar Agent
        
        Args:
            app_name: Application name
        """
        self.app_name = app_name
        self.agent = self._create_agent()
        self.runner = self._create_runner()
        
    def _create_agent(self) -> Agent:
        """
        Create the Trend Radar Agent instance
        
        Returns:
            Agent: Configured Agent instance
        """
        # 使用LiteLlm包装器配置模型
        model_config = get_model_config(MODEL_GEMINI_1_5_PRO)
        model = LiteLlm(
            model=model_config["model"],
            api_key=model_config["api_key"],
            base_url=model_config["base_url"]
        )
        
        # Create crawler tool (placeholder implementation)
        crawler_tool = FunctionTool(
            func=self._crawl_platform_trends
        )
        
        return Agent(
            name="trend_radar_agent",
            model=model,  # 使用LiteLlm包装的模型
            description="Identifies trending topics, keywords, and content directions for e-commerce platforms",
            instruction="""
            You are the Trend Radar Agent for Marketa-Pro. Your role is to identify and analyze 
            current trends on various e-commerce platforms to inform content strategy.
            
            Your primary responsibilities include:
            1. Identifying trending topics, keywords, and hashtags on the specified platform
            2. Analyzing content formats and styles that are performing well 
            3. Determining optimal posting times and engagement patterns
            4. Recognizing emerging trends relevant to specific product categories
            5. Providing actionable trend insights that can be used for content creation

            When you receive a request:
            1. Use the crawl_platform_trends tool to gather raw trend data from the specified platform
            2. Analyze the data to extract meaningful patterns and insights
            3. Organize your findings into a structured trend analysis report
            
            Your output should be a comprehensive trend analysis with the following sections:
            
            ## Current Platform Trends
            [List of 3-5 trending content types or themes, with engagement metrics when available]
            
            ## Relevant Hashtags
            [List of 5-7 hashtags that are trending and relevant to the product category]
            
            ## Content Format Recommendations
            [3-4 content formats that are performing well, with engagement metrics when available]
            
            ## Optimal Posting Times
            [Recommended times for posting based on engagement patterns]
            
            ## Emerging Conversations
            [Topics or questions that are starting to gain traction in this product category]
            
            Ensure your analysis is specific to the platform indicated in the request and relevant 
            to the product category provided.
            """,
            tools=[crawler_tool],
        )
    
    def _create_runner(self) -> Runner:
        """
        Create Runner instance to execute the Agent
        
        Returns:
            Runner: Configured Runner instance
        """
        return Runner(
            agent=self.agent,
            app_name=self.app_name,
            session_service=InMemorySessionService(),
        )
    
    def _crawl_platform_trends(self, 
                             platform: str, 
                             product_category: str,
                             tool_context: ToolContext) -> Dict[str, Any]:
        """
        Placeholder function for crawling trend data from specified platform
        
        Args:
            platform: The e-commerce platform to crawl (e.g., 'xiaohongshu', 'tiktok')
            product_category: The product category to focus on
            tool_context: Context provided by the Agent framework
            
        Returns:
            Dict: Trend data in structured format
        """
        # In a real implementation, this would use a crawler/scraper to get actual trend data
        # For now, we'll return simulated trend data based on the platform and category
        logger.info(f"Placeholder: Crawling trend data from {platform} for category: {product_category}")
        
        # Simulated trend data
        if platform.lower() == "xiaohongshu":
            return {
                "trending_topics": [
                    {"topic": "Morning routine", "engagement_rate": 5.8},
                    {"topic": "Minimalist lifestyle", "engagement_rate": 4.9},
                    {"topic": "Tech accessories", "engagement_rate": 4.2},
                    {"topic": "Health tracking", "engagement_rate": 3.7}
                ],
                "trending_hashtags": [
                    "#SmartLiving", "#MorningRoutine", "#TechForHealth", 
                    "#HydrationCheck", "#MinimalistTech", "#DailyHacks", "#ProductivityTools"
                ],
                "content_formats": [
                    {"format": "Carousel posts with product details", "conversion_rate": "32%"},
                    {"format": "Day-in-the-life videos", "popularity": "High with 25-35 demographic"},
                    {"format": "Product comparison content", "comment_rate": "2.3x average"},
                    {"format": "Unboxing experiences", "save_rate": "28% higher than average"}
                ],
                "optimal_posting_times": [
                    {"time_range": "7-9 AM weekdays", "content_type": "routine-based content"},
                    {"time_range": "12-1 PM weekdays", "content_type": "productivity content"},
                    {"time_range": "7-9 PM Sunday", "content_type": "planning/aspirational content"}
                ],
                "emerging_conversations": [
                    "Sustainable tech accessories",
                    "Multi-function smart devices",
                    "Health data integration across devices"
                ]
            }
        elif platform.lower() == "tiktok":
            return {
                "trending_topics": [
                    {"topic": "Tech unboxing", "engagement_rate": 6.3},
                    {"topic": "Life hacks", "engagement_rate": 5.7},
                    {"topic": "Product reviews", "engagement_rate": 4.8},
                    {"topic": "Quick tutorials", "engagement_rate": 4.4}
                ],
                "trending_hashtags": [
                    "#TechTok", "#SmartHome", "#ReviewTime", "#LifeHack", 
                    "#MustHaveProducts", "#TrendingNow", "#UnboxingTime"
                ],
                "content_formats": [
                    {"format": "15-second demo videos", "view_completion": "78%"},
                    {"format": "Before/after comparison", "sharing_rate": "2.1x average"},
                    {"format": "POV usage scenarios", "comment_rate": "3.4x average"},
                    {"format": "Duet reviews", "conversion_rate": "24% higher than solo reviews"}
                ],
                "optimal_posting_times": [
                    {"time_range": "9-11 AM weekdays", "content_type": "informational content"},
                    {"time_range": "3-5 PM weekdays", "content_type": "entertaining content"},
                    {"time_range": "8-10 PM all days", "content_type": "trending challenges"}
                ],
                "emerging_conversations": [
                    "Tech that simplifies daily routines",
                    "Aesthetic tech accessories",
                    "Products that content creators use"
                ]
            }
        else:
            # Default generic trends
            return {
                "trending_topics": [
                    {"topic": "Product reviews", "engagement_rate": 4.1},
                    {"topic": "Lifestyle integration", "engagement_rate": 3.9},
                    {"topic": "Value comparison", "engagement_rate": 3.5}
                ],
                "trending_hashtags": [
                    "#MustHave", "#TrendingNow", "#NewLaunch", "#CustomerReviews", "#TopPicks"
                ],
                "content_formats": [
                    {"format": "Short video reviews", "popularity": "High across demographics"},
                    {"format": "Image galleries", "engagement_rate": "Good for product details"},
                    {"format": "User testimonials", "conversion_rate": "Higher trust factor"}
                ],
                "optimal_posting_times": [
                    {"time_range": "10 AM - 1 PM", "content_type": "informational content"},
                    {"time_range": "6 PM - 9 PM", "content_type": "entertainment content"}
                ],
                "emerging_conversations": [
                    "Product sustainability",
                    "Value for money",
                    "Integration with other products"
                ]
            }
    
    async def analyze_platform_trends(self, 
                                 platform: str, 
                                 product_category: str,
                                 product_tags: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Analyze trends for a specific platform and product category
        
        Args:
            platform: The e-commerce platform to analyze (e.g., 'xiaohongshu', 'tiktok')
            product_category: The product category to focus on
            product_tags: Optional list of product tags to consider
            
        Returns:
            Dict: Trend analysis results
        """
        # Create session ID
        session_id = f"trend_analysis_{platform}_{product_category}"
        
        try:
            # Format query for the agent
            query = self._format_query(platform, product_category, product_tags)
            
            # Call Agent for processing
            trend_result = await self.runner.run(
                query=query,
                session_id=session_id
            )
            
            return {
                "status": "success",
                "session_id": session_id,
                "trend_analysis": trend_result,
                "platform": platform,
                "product_category": product_category
            }
            
        except Exception as e:
            logger.error(f"Error analyzing platform trends: {str(e)}")
            return {
                "status": "failed",
                "session_id": session_id,
                "error": str(e),
                "platform": platform,
                "product_category": product_category
            }
    
    def _format_query(self, 
                  platform: str, 
                  product_category: str, 
                  product_tags: Optional[List[str]] = None) -> str:
        """
        Format platform and category into a query string for the Agent
        
        Args:
            platform: The e-commerce platform to analyze
            product_category: The product category to focus on
            product_tags: Optional list of product tags
            
        Returns:
            str: Formatted query string
        """
        tags_str = ", ".join(product_tags) if product_tags else "Not specified"
        
        query = f"""
        Please analyze current trends on {platform} for the {product_category} category.
        
        Product tags: {tags_str}
        
        Use the crawl_platform_trends tool to gather trend data, then analyze the results 
        to provide a comprehensive trend analysis report.
        """
        
        return query

# Usage example
async def example_usage():
    trend_analyzer = TrendRadarAgent()
    
    # Example usage
    platform = "xiaohongshu"
    product_category = "smart home devices"
    product_tags = ["technology", "smart cup", "health", "lifestyle"]
    
    result = await trend_analyzer.analyze_platform_trends(
        platform=platform,
        product_category=product_category,
        product_tags=product_tags
    )
    
    print(f"Trend analysis result: {result}") 