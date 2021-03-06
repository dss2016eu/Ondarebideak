from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.db.models import Q
from django.utils.translation import ugettext as _
from django.db.models import Count
#from haystack import site






#from pg_fts.fields import TSVectorField


#Laguntza: https://docs.djangoproject.com/en/1.8/ref/models/fields/#model-field-types
#https://docs.djangoproject.com/en/1.8/topics/db/models/#field-types


class lizentzia(models.Model):
    izena=models.TextField()
    url=models.TextField()
    ikonoa=models.TextField()

#Desciption: Information on resources imported from Alinari and Europeana, corresponding to the EDM specification.
#Primary key constraint name: PK_item 
class item(models.Model):
    #id = models.IntegerField(primary_key=True) 
    fk_ob_user = models.ForeignKey(User)
    uri = models.CharField(max_length=250, unique=True) #unique=tue beharrezkoa da, beste taula batzuk Fk bezala erabiltzen dute eta
    usfd_id = models.CharField(max_length=3000)
    dc_title = models.TextField()
    dc_creator = models.TextField()
    dc_subject = models.TextField()
    dc_description = models.TextField()
    dc_publisher = models.TextField()
    dc_contributor = models.TextField()
    dc_date=models.TextField()
    dc_type=models.TextField()
    dc_format=models.TextField()
    dc_identifier=models.TextField()
    dc_source=models.TextField()
    dc_language=models.TextField()
    dc_relation=models.TextField()
    dc_rights=models.TextField()
    dc_coverage=models.TextField()
    dcterms_provenance=models.TextField()
    dcterms_ispartof=models.TextField()
    dcterms_temporal=models.TextField()
    dcterms_spatial=models.TextField()
    dcterms_medium=models.TextField()
    dcterms_extent=models.TextField()
    dcterms_alternative=models.TextField()
    dcterms_issued=models.TextField()
    dcterms_tableofcontents=models.TextField()
    dcterms_isreplacedby=models.TextField()
    edm_unstored=models.TextField()
    edm_object=models.TextField()
    edm_provider=models.TextField()
    edm_type=models.TextField()
    edm_rights=models.TextField()
    edm_dataprovider=models.TextField()
    edm_isshownby=models.TextField()
    edm_isshownat=models.TextField()
    edm_country=models.TextField()
    edm_language=models.TextField()
    edm_uri=models.TextField()
    edm_usertag=models.TextField()
    edm_year=models.CharField(max_length=1000)
    edm_previewnodistribute=models.TextField()
    edm_hasobject=models.TextField()
    paths_bow=models.TextField()
    paths_facet_date=models.CharField(max_length=1000)
    paths_informativeness=models.FloatField(null=True)
    paths_trav_count=models.IntegerField(null=True)
    proposatutakoa = models.BooleanField(default=False)
    egunekoa = models.BooleanField(default=False)
    geoloc_longitude = models.FloatField(null=True)
    geoloc_latitude = models.FloatField(null=True)
    aberastua = models.BooleanField(default=False)
    ob_language=models.TextField()
    # idxfti=models.TSVectorField('dc_title')
    #objects = ProposalManager()
    
    def __unicode__(self):
        return self.dc_title
    
    # botoak lortu
    def get_votes(self):
        votes = votes_item.objects.filter(item = self)
        votes_count = len(votes)
        
        return votes_count

    #boto bat eman
    def vote(self, user):
        try:
            
            # user vote number
            user_votes = votes_item.objects.filter(user = user.id)
           
            item_user_votes = user_votes.filter(item = self)
            # check  user's votes in the project
            if len(item_user_votes) == 0:
                vote = votes_item()
                vote.item = self
                vote.user = user
                vote.save()
                return True
            else:
                return False
        except Exception as error:
            print error
            return False
    
    #botoa kendu
    def unvote(self,user):
        try:
            
            # user vote number
            user_votes = votes_item.objects.filter(user = user.id)
           
            item_user_votes = user_votes.filter(item = self)
            # check  user's votes in the project
            if len(item_user_votes) == 0:
                return False
               
            else:              
                votes_item.objects.filter(item = self,user = user).delete()             
                return True
        except Exception as error:
            print error
            return False
        
    #Itemei dagokien QR kodeak sortzeko erabiliko da
    def get_absolute_url(self):
        return "http://ondarebideak.dss2016.eu/erakutsi_item?id=%i" % self.id
      
    # get comments
    def get_comments(self):
        return itemComment.objects.filter(itema=self,parent_comment=None).order_by('-id')
        
    def get_all_comments(self):
        return itemComment.objects.filter(itema=self).order_by('-id') 
    
class votes_item(models.Model):
    item = models.ForeignKey(item)
    user = models.ForeignKey(User)
    


class itemCommentManager(models.Manager):

    def create_comment(self,\
                    comment,\
                    item,\
                    user,\
                    parent):
        item_comment = itemComment()
        item_comment.comment = comment
        item_comment.author = user
        item_comment.itema = item
        item_comment.parent_comment = parent
        item_comment.save()
        return item_comment


class itemComment(models.Model):
    itema = models.ForeignKey(item)
    comment = models.TextField()
    parent_comment = models.ForeignKey("self",null=True)
    #author = models.ForeignKey(Profile)
    author = models.ForeignKey(User)
    date = models.DateField(auto_now = True, null = True)
    
    objects = itemCommentManager()
    
    def get_subcomments(self):
        return self.itemcomment_set.all()

    
#Description:Links between Items and external background resources (e.g. Wikipedia) as derived from semantic processing.
#class item_link(models.Model):
    #id = models.IntegerField(primary_key=True) 
    #fk_rel_uri = models.ForeignKey('item',to_field='uri') #!! honek errorea eman dezake. Bestela Item-en id-ra lotuta sortu ForeigKey-a
    #source = models.CharField(max_length=1000)
    #field = models.CharField(max_length=1000)
    #start_offset = models.IntegerField()
    #end_offset = models.IntegerField()
    #confidence = models.FloatField() # Paths-en NUMERIC motakoa da
    #method = models.CharField(max_length=1000)
    #title = models.CharField(max_length=1000)
    #link = models.CharField(max_length=1000)
    #sentiment = models.FloatField()# Paths-en NUMERIC motakoa da
    #paths_classification = models.CharField(max_length=1000)
    
#Description: Information on similarity between Items as derived from semantic processing.
#class item_similarity(models.Model):
    #id = models.IntegerField(primary_key=True) 
    #fk_sitem_uri = models.ForeignKey('item',to_field='uri', related_name='source_similarity') #!! honek errorea eman dezake. Bestela Item-en id-ra lotuta sortu ForeigKey-a
    #fk_titem_uri = models.ForeignKey('item',to_field='uri', related_name='target_similarity') #!! honek errorea eman dezake. Bestela Item-en id-ra lotuta sortu ForeigKey-a
    #field = models.CharField(max_length=1000)
    #field_no = models.IntegerField()
    #start_offset = models.IntegerField()
    #end_offset = models.IntegerField()
    #confidence = models.FloatField() # Paths-en NUMERIC motakoa da
    #method=models.CharField(max_length=1000)
    #title=models.CharField(max_length=1000)
    #sentiment = models.FloatField()# Paths-en NUMERIC motakoa da

#Description:Information on which Items a user has traversed between.

#class behaviour_link(models.Model):
    #id = models.IntegerField(primary_key=True) 
    #fk_rel_suri = models.ForeignKey('item',to_field='uri', related_name='source_behaviour') #Source URI resource (the URI of the resource the user came from)
    #fk_rel_turi = models.ForeignKey('item',to_field='uri', related_name='target_behaviour') #Target URI resource (the URI of the resource the user browsed to)
    #avg_time = models.IntegerField() #Average time at target URI in seconds
    #trav_count = models.IntegerField() #Number of times the link has been traversed.


#Description:Information about topic hierarchies
#class topic(models.Model):
    #id = models.IntegerField(primary_key=True)
    #fk_parent_topic_ids = models.CharField(max_length=1000)  # Hau array bat da Paths-en. Topic gurasoen id-ak dira. Guk string bat erabiliko dugu komaz bereizia
    #uri = models.CharField(max_length=1000) #Automatically generated uri at the time of creating a new record
    #dc_title = models.CharField(max_length=1000)

#Description: Many to many table between item and topic. One topic may have many items, one item may have many topics.
#class item_topic(models.Model):
    #id = models.IntegerField(primary_key=True) 
    #fk_item_uri = models.ForeignKey('item',to_field='uri') #!! honek errorea eman dezake. Bestela Item-en id-ra lotuta sortu ForeigKey-a
    #fk_topic_id = models.ForeignKey('topic') #to_field='id' , defektuzkoa da
    
#Description: This table also contains the column "geom" that holds WKT POINT geometries. This is added using the PostGIS AddGeomColumn function after creation of the table.
#class map_point (models.Model):
    #id = models.IntegerField(primary_key=True)
    #item_id = models.ForeignKey('item', related_name='current') #to_field='id' , defektuzkoa da
    #dc_title = models.CharField(max_length=1000)
    #parent_id = models.ForeignKey('item', related_name='parent') #to_field='id' , defektuzkoa da
    #dc_type = models.CharField(max_length=1000)
   
#Description: This table also contains the column "geom" that holds WKT POLYGON geometries.
# This is added using the PostGIS AddGeomColumn function aftercreation of the table.   
#class map_poly (models.Model):
    #id = models.IntegerField(primary_key=True)
    #dc_title = models.CharField(max_length=1000)
    #topic_id = models.ForeignKey('topic') #to_field='id' , defektuzkoa da
    #parent_id = models.ForeignKey('item') #to_field='id' , defektuzkoa da
    #dc_type = models.CharField(max_length=1000)
    #m_order = models.IntegerField()

#Description:Codelist of different cognitive styles. A user may have one cognitive style.
#class cog_style (models.Model):
    #id = models.IntegerField(primary_key=True)
    #title= models.CharField(max_length=1000)



#Description: Information about users such as username, password, nickname etc.
#Djangok automatikoki sortutako auth_user heredatzen du

#+--------------+--------------+------+-----+---------+----------------+
#| Field        | Type         | Null | Key | Default | Extra          |
#+--------------+--------------+------+-----+---------+----------------+
#| id           | int(11)      | NO   | PRI | NULL    | auto_increment |
#| password     | varchar(128) | NO   |     | NULL    |                |
#| last_login   | datetime     | YES  |     | NULL    |                |
#| is_superuser | tinyint(1)   | NO   |     | NULL    |                |
#| username     | varchar(30)  | NO   | UNI | NULL    |                |
#| first_name   | varchar(30)  | NO   |     | NULL    |                |
#| last_name    | varchar(30)  | NO   |     | NULL    |                |
#| email        | varchar(254) | YES  |     | NULL    |                |
#| is_staff     | tinyint(1)   | NO   |     | NULL    |                |
#| is_active    | tinyint(1)   | NO   |     | NULL    |                |
#| date_joined  | datetime     | NO   |     | NULL    |                |
#+--------------+--------------+------+-----+---------+----------------+

class usr (models.Model):
    user = models.OneToOneField(User)  #Hemen heredatzen dira Djangon User taulako eremuak 
    #fk_cog_style_id = models.ForeignKey('cog_style') # The id of the cognitive style associated with the user
    uri =  models.CharField(max_length=1000) # Automatically generated uri at the time of creating a new record
    foaf_nick = models.CharField(max_length=1000)
    email_visibility = models.CharField(max_length=100) #Value that indicates whether the e-mail address of the user shall be publicly displayed in the user interface. In web services also referred to as "foaf_mbox_visibility" 
    openid = models.BooleanField(default=True) #Boolean value indicating whether the account belongs to an OpenID provider
    isdeleted = models.BooleanField(default=False)
    istemporary = models.BooleanField(default=False)
    tstamp =models.DateField(auto_now_add=True)
    #Heredatuak:
    #id
    #password (paths-en 'pwd')
    #email
    
    

    
#Description:Information about paths such as title, subject, description etc.
class path (models.Model):
    #id = models.IntegerField(primary_key=True)
    fk_user_id = models.ForeignKey(User)
    uri = models.CharField(max_length=1000) # Automatically generated uri at the time of creating a new record
    dc_title = models.CharField(max_length=1000) #Title of path, taken from Dublin Core namespace
    dc_subject = models.CharField(max_length=1000) # Subject of path, taken from Dublin Core namespace. Multiple values are separated by semi-colon ";"
    dc_description = models.TextField()
    acces = models.CharField(max_length=1000) #Any access restrictions associated with path
    lom_length = models.CharField(max_length=1000) #Approximate time required/duration of path, taken from Learning Object Model namespace.
    isdeleted = models.BooleanField(default=False)
    paths_status = models.CharField(max_length=1000) #A boolean attribute that indicates whether the path is public or not.
    paths_thumbnail = models.CharField(max_length=1000) # The complete URI of a thumbnail specifically chosen for this path - not derived from the items 
    paths_iscloneable = models.BooleanField(default=False)
    tstamp =models.DateField(auto_now_add=True)
    creation_date = models.DateField(auto_now_add=True)
    proposatutakoa = models.BooleanField(default=False)
    egunekoa = models.BooleanField(default=False)
    language=models.TextField() #eu,es,en
    
        
    # botoak lortu
    def get_votes(self):
        votes = votes_path.objects.filter(path = self)
        votes_count = len(votes)
        
        return votes_count

    #boto bat eman
    def vote(self, user):
        try:
            # user vote number
            user_votes = votes_path.objects.filter(user = user.id)
            path_user_votes = user_votes.filter(path = self)
            # check  user's votes in the project
            if len(path_user_votes) == 0:
                vote = votes_path()
                vote.path = self
                vote.user = user
                vote.save()
                return True
            else:
                return False
        except Exception as error:
            print error
            return False

    #botoa kendu
    def unvote(self,user):
        try:
            
            # user vote number
            user_votes = votes_path.objects.filter(user = user.id)
           
            path_user_votes = user_votes.filter(path = self)
            # check  user's votes in the project
            if len(path_user_votes) == 0:
                return False
               
            else:              
                votes_path.objects.filter(path = self,user = user).delete()             
                return True
        except Exception as error:
            print error
            return False
    
    # get comments
    def get_comments(self):
        return pathComment.objects.filter(patha=self,parent_comment=None).order_by('-id')
        
    def get_all_comments(self):
        return pathComment.objects.filter(patha=self).order_by('-id') 
    
class votes_path(models.Model):
    path = models.ForeignKey(path)
    user = models.ForeignKey(User)   



class pathCommentManager(models.Manager):

    def create_comment(self,\
                    comment,\
                    path,\
                    profile,\
                    parent):
        path_comment = pathComment()
        path_comment.comment = comment
        path_comment.author = profile
        path_comment.patha = path
        path_comment.parent_comment = parent
        path_comment.save()
        return path_comment


class pathComment(models.Model):
    patha = models.ForeignKey(path)
    comment = models.TextField()
    parent_comment = models.ForeignKey("self",null=True)
    #author = models.ForeignKey(Profile)
    author = models.ForeignKey(User)
    date = models.DateField(auto_now = True, null = True)
    
    objects = pathCommentManager()
    
    def get_subcomments(self):
        return self.pathcomment_set.all()

   
#Description: Comments added to objects identifiable by a URI      
#class comment(models.Model):
    #id = models.IntegerField(primary_key=True)
    #fk_user_id = models.ForeignKey('usr') # Id of user creating comment
    #fk_rel_uri = models.ForeignKey('item') #URI of resource which comment is assigned to
    #comment = models.TextField()
    #isdeleted =models.BooleanField(default=False)
    #tstamp = models.DateField(auto_now_add=True)
    
#Description: Information about path nodes such as title, description, node_order etc.    
class node (models.Model):
    #id = models.IntegerField(primary_key=True)
    fk_item_id = models.ForeignKey(item)
    uri = models.CharField(max_length=3000) # Automatically generated uri at the time of creating a new record
    fk_path_id = models.ForeignKey(path)
    dc_source = models.CharField(max_length=1000)
    dc_title = models.TextField()
    dc_description = models.TextField()
    type = models.CharField(max_length=1000) # For example: image, text etc.
    paths_thumbnail = models.CharField(max_length=1000) # Filename of a thumbnail explicitly chosen for the  espective node. Not derived from the item.
    paths_prev = models.CharField(max_length=1000) # komaz bereizitako lista bat  PATHS: Array of node URIs for nodes that are "before" the present node within a path. Introduced to support branching paths.
    paths_next = models.CharField(max_length=1000) # komaz bereizitako lista bat  PATHS: Array of node URIs for nodes that are "before" the present node within a path. Introduced to support branching paths.
    paths_start =models.BooleanField(default=False) # A boolean value that is set to true on any node where a path can start, i.e. where there are no node identifiers in paths_prev.
    isdeleted =models.BooleanField(default=False) # A boolean value that indicates whether a node has been deleted. True =deleted, false = not deleted.    
    tstamp = models.DateField(auto_now_add=True)
    geoloc_longitude = models.FloatField(null=True)
    geoloc_latitude = models.FloatField(null=True)
    
#Description: Rating scale for paths and other resources identifiable by a URI. 1 = dislikes, 2 =likes.
#class rating_scale (models.Model):
    #id = models.IntegerField(primary_key=True)
    #label = models.CharField(max_length=1000)

  
#Description: Assigns a rating to any resource identifiable by a URI. Rating is linked to a rating scale and a user. A user is only allowed to rate a URI resource once.    
#class rating (models.Model):
    #id = models.IntegerField(primary_key=True)
    #fk_usr_id = models.ForeignKey('usr')
    #fk_rating_scale_id = models.ForeignKey('rating_scale')
    #fk_rel_uri = models.CharField(max_length=1000)
    #isdeleted =models.BooleanField(default=False)

#Description:Tags: keywords and keyphrases assigned to URI resources. Tags may be language specific and are identifiable by a URI.    
#class tag (models.Model):
    #id = models.IntegerField(primary_key=True)
    # uri = models.CharField(max_length=1000)# Automatically generated uri at the time of creating a new record
    #label = models.CharField(max_length=1000)
    #lang = models.CharField(max_length=1000)
    
#Description: Association between tags, users and resources identifiable by a URI. A user can only add the same keyword to a resource once.
#class tagging (models.Model):
    #id = models.IntegerField(primary_key=True)
    #fk_tag_id = models.ForeignKey('tag')
    #fk_usr_id = models.ForeignKey('usr')
    # fk_rel_uri = models.ForeignKey('item', to_field='uri') # ??
    # isdeleted =models.BooleanField(default=False)

#Description:     
#class uaction (models.Model):
    #id = models.IntegerField(primary_key=True)
    #fk_usr_id = models.ForeignKey('usr')
    #usession = models.CharField(max_length=1000)
    #dc_source = models.CharField(max_length=1000)
    #paths_request = models.TextField()
    #tstamp = models.DateField(auto_now_add=True)

#Description: Information on the way users navigate through information in the PATHS database.    
#class ubehaviour (models.Model):
    #id = models.IntegerField(primary_key=True)
    #fk_usr_id = models.ForeignKey('usr')
    #usession = models.CharField(max_length=1000)
    #dc_title = models.CharField(max_length=1000) #URI of object user is navigating from
    #dc_source = models.CharField(max_length=1000)
    #tstamp = models.DateField(auto_now_add=True)
    
#Description:Codelist of user groups used to distinguish what privieges each user has in the
#PATHS system. New users by default are members of the 'user' group (id=1).
#Administrator users are members of the 'admin' group (id=2). New groups may be
#added to further differentiate privileges.

#mysql> describe auth_group;
#+-------+-------------+------+-----+---------+----------------+
#| Field | Type        | Null | Key | Default | Extra          |
#+-------+-------------+------+-----+---------+----------------+
#| id    | int(11)     | NO   | PRI | NULL    | auto_increment |
#| name  | varchar(80) | NO   | UNI | NULL    |                |
#+-------+-------------+------+-----+---------+----------------+

#class ugroup (Group):
#   id = models.IntegerField(max_length=10, primary_key=True)
#  title = models.CharField(max_length=1000)
    


#mysql> describe auth_user_groups;
#+----------+---------+------+-----+---------+----------------+
#| Field    | Type    | Null | Key | Default | Extra          |
#+----------+---------+------+-----+---------+----------------+
#| id       | int(11) | NO   | PRI | NULL    | auto_increment |
#| user_id  | int(11) | NO   | MUL | NULL    |                |
#| group_id | int(11) | NO   | MUL | NULL    |                |
#+----------+---------+------+-----+---------+----------------+

#Description: Many-to-many relationship table between users and user groups.
#class usr_ugroup (models.Model):
#    id = models.IntegerField(max_length=10, primary_key=True)
#    fk_usr_id = models.ForeignKey('usr')
#    fk_ugroup_id = models.ForeignKey('ugroup')
    

class workspace(models.Model):
    #id = models.IntegerField(primary_key=True)
    fk_usr_id = models.ForeignKey(User)
    uri = models.CharField(max_length=3000)
    tstamp = models.DateField(auto_now_add=True)
    isprimary = models.BooleanField(default=True)
    
#Description:Temporary storage table for half-baked nodes and items that a user wants to add
#to PATHS at a later stage after working on them. 
#class usr_workspace(models.Model):
    #id = models.IntegerField(primary_key=True)
    #fk_usr_id = models.ForeignKey('usr')
    #fk_workspace_id = models.ForeignKey('workspace')

#Description:Temporary storage table for half-baked nodes and items that a user wants to add
#to PATHS at a later stage after working on them.
class workspace_item(models.Model):
    #id = models.IntegerField(primary_key=True)
    fk_item_id = models.ForeignKey(item)
    uri = models.CharField(max_length=3000)
    fk_workspace_id = models.ForeignKey(workspace)
    dc_source = models.CharField(max_length=1000)
    dc_title = models.CharField(max_length=1000) 
    dc_description = models.TextField()
    type = models.CharField(max_length=1000)
    paths_thumbnail = models.CharField(max_length=1000)


class hornitzailea(models.Model):
    
    fk_user= models.ForeignKey(User)
    izena=models.CharField(max_length=1000)
    deskribapena = models.CharField(max_length=3000)
    erakundeMota = models.CharField(max_length=1000)
    ikonoa = models.CharField(max_length=1000)
    argazkia = models.CharField(max_length=1000)
    telefonoa = models.CharField(max_length=1000)
    emaila = models.CharField(max_length=1000)
    website = models.CharField(max_length=1000)
    ordutegia = models.CharField(max_length=1000)
    helbidea = models.CharField(max_length=1000)
    geoloc_longitude = models.FloatField(null=True)
    geoloc_latitude = models.FloatField(null=True)
    
    
    
class ProfileManager(models.Manager):
    
    def create_profile(self,\
                    username,\
                    name,\
                    surname,\
                    email,\
                    hornitzailea,\
                    hornitzaile_izena,\
                    herrialdea,\
                    password):
        """Creates a new profile"""      
        profile = Profile()        
        profile.hornitzailea = hornitzailea
        profile.hornitzaile_izena = hornitzaile_izena
        profile.herrialdea = herrialdea
        # Create a user object  
        user = User.objects.create_user(first_name = name,last_name = surname, username = username, email = email, password = password)
        group = Group.objects.get(name='arrunta') 
        group.user_set.add(user)
        profile.user = user
        profile.save()
        return profile





class Profile(models.Model):
    user = models.OneToOneField(User) 
    hornitzailea = models.NullBooleanField()
    hornitzaile_izena = models.CharField(max_length=100,null=True)
    herrialdea = models.CharField(max_length=100,null=True)
         
    objects = ProfileManager()

    
    def is_admin(self):
        group = Group.objects.get(name="admin")
        return True if group in self.user.groups.all() else False
        
    def is_hornitzailea(self):
        group = Group.objects.get(name="hornitzailea")
        return True if group in self.user.groups.all() else False
        
    def is_arrunta(self):
        group = Group.objects.get(name="arrunta")
        return True if group in self.user.groups.all() else False
        
    def has_advanced_permissions(self):
        return self.is_admin() or self.is_manager()



    
    
