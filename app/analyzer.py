class Analyzer:
    def process_leads(self, raw_leads, niche):
        """
        Cleans and formats raw scraped leads before saving to DB and passing to AI.
        """
        processed = []
        for lead in raw_leads:
            # Ensure required fields
            business_name = lead.get('business_name', 'Unknown Business')
            profile_url = lead.get('profile_url', '')
            
            if not profile_url:
                continue
                
            processed.append({
                "business_name": business_name,
                "niche": niche,
                "profile_url": profile_url,
                "bio": lead.get('bio', ''),
                "follower_estimate": lead.get('follower_estimate', 'Unknown'),
                "contact_info": lead.get('contact_info', 'None')
            })
            
        return processed
