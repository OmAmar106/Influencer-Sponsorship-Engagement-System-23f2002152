# Influencer Sponsorship Engagement System  

This repository contains the **MAD-I Project** by **Om Amar (23f2002152)**, developed during the **May-September term**.  

This project is a comprehensive **Influencer Sponsorship Engagement System** that simplifies the collaboration process between **Sponsors** and **Influencers**. It includes a variety of features for sponsors, influencers, and admins to manage their tasks effectively.

---

## Features  

1. **Profile Management**  
   - Create **Sponsor** and **Influencer** profiles.  

2. **Campaign Creation**  
   - Sponsors can create **ads/campaigns** and send requests to Influencers.  
   - Influencers can also request campaigns from Sponsors.  

3. **Negotiation Platform**  
   - Campaign requests between **Sponsors** and **Influencers** can be negotiated.  

4. **Admin Controls**  
   - Admins can view **website statistics**, **ban users**, and **flag inappropriate campaigns/ads**.  

5. **Search and Filtering**  
   - Users and campaigns can be searched using **various filters**.  

6. **Profile Picture Updates**  
   - Users can update their **profile pictures**.  

---

## Installation  

To install the required dependencies, run the following command:  

```bash
>>pip3 install Flask
```
```bash
>>pip3 install Flask-SQLAlchemy
```

After this , go to the folder in which you have downloaded the file followed by

```bash
>>cd MAD-I_Project
```
```bash
>>python main.py
```

# Some Screenshots <br>
<br>![signupform](https://github.com/OmAmar106/Influencer-Sponsorship-System-23f2002152/assets/142908269/d5e3a10c-a592-4049-beb1-b8b8774d5025)<br>
<br>![campaign](https://github.com/OmAmar106/Influencer-Sponsorship-System-23f2002152/assets/142908269/7357e27f-ea3d-4f06-a6b5-f3e969fa7266)<br>
<br>![usersearch](https://github.com/OmAmar106/Influencer-Sponsorship-System-23f2002152/assets/142908269/b0a004fe-d145-4b02-b8f7-7496a2545975)<br>

<br>API End Points : <br><br>
For users : 
<pre>>> /api/user/userid </pre>
For ads : 
<pre>>> /api/ad/adname</pre>
For Campaigns : 
<pre>>> /api/campaign/campaignname</pre>
