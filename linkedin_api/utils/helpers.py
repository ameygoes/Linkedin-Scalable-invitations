import random
import base64
import uuid

def generateUUID():
    # Generate a random UUID
    return str(uuid.uuid4())

def get_id_from_urn(urn):
    """
    Return the ID of a given Linkedin URN.

    Example: urn:li:fs_miniProfile:<id>
    """
    return urn.split(":")[3]

def get_updated_urn(string):    
    return f"urn:li:fsd_invitation:{get_id_from_urn(string)}"

def get_urn_from_raw_update(raw_string):
    """
    Return the URN of a raw group update

    Example: urn:li:fs_miniProfile:<id>
    Example: urn:li:fs_updateV2:(<urn>,GROUP_FEED,EMPTY,DEFAULT,false)
    """
    return raw_string.split("(")[1].split(",")[0]


def get_update_author_name(d_included):
    """Parse a dict and returns, if present, the post author name

    :param d_included: a dict, as returned by res.json().get("included", {})
    :type d_raw: dict

    :return: Author name
    :rtype: str
    """
    try:
        return d_included["actor"]["name"]["text"]
    except KeyError:
        return ""
    except TypeError:
        return "None"


def get_update_old(d_included):
    """Parse a dict and returns, if present, the post old string

    :param d_included: a dict, as returned by res.json().get("included", {})
    :type d_raw: dict

    :return: Post old string. Example: '2 mo'
    :rtype: str
    """
    try:
        return d_included["actor"]["subDescription"]["text"]
    except KeyError:
        return ""
    except TypeError:
        return "None"


def get_update_content(d_included, base_url):
    """Parse a dict and returns, if present, the post content

    :param d_included: a dict, as returned by res.json().get("included", {})
    :type d_raw: dict
    :param base_url: site URL
    :type d_raw: str

    :return: Post content
    :rtype: str
    """
    try:
        return d_included["commentary"]["text"]["text"]
    except KeyError:
        return ""
    except TypeError:
        # Let's see if its a reshared post...
        try:
            # TODO: call Linkedin API to fetch that particular post and extract content
            urn = get_urn_from_raw_update(d_included["*resharedUpdate"])
            return f"{base_url}/feed/update/{urn}"
        except KeyError:
            return "IMAGE"
        except TypeError:
            return "None"


def get_update_author_profile(d_included, base_url):
    """Parse a dict and returns, if present, the URL corresponding the profile

    :param d_included: a dict, as returned by res.json().get("included", {})
    :type d_raw: dict
    :param base_url: site URL
    :type d_raw: str

    :return: URL with either company or member profile
    :rtype: str
    """
    try:
        urn = d_included["actor"]["urn"]
    except KeyError:
        return ""
    except TypeError:
        return "None"
    else:
        urn_id = urn.split(":")[-1]
        if "company" in urn:
            return f"{base_url}/company/{urn_id}"
        elif "member" in urn:
            return f"{base_url}/in/{urn_id}"


def get_update_url(d_included, base_url):
    """Parse a dict and returns, if present, the post URL

    :param d_included: a dict, as returned by res.json().get("included", {})
    :type d_raw: dict
    :param base_url: site URL
    :type d_raw: str

    :return: post url
    :rtype: str
    """
    try:
        urn = d_included["updateMetadata"]["urn"]
    except KeyError:
        return ""
    except TypeError:
        return "None"
    else:
        return f"{base_url}/feed/update/{urn}"


def append_update_post_field_to_posts_list(d_included, l_posts, post_key, post_value):
    """Parse a dict and returns, if present, the desired value. Finally it
    updates an already existing dict in the list or add a new dict to it

    :param d_included: a dict, as returned by res.json().get("included", {})
    :type d_raw: dict
    :param l_posts: a list with dicts
    :type l_posts: list
    :param post_key: the post field name to extract. Example: 'author_name'
    :type post_key: str
    :param post_value: the post value correspoding to post_key
    :type post_value: str

    :return: post list
    :rtype: list
    """
    elements_current_index = len(l_posts) - 1

    if elements_current_index == -1:
        l_posts.append({post_key: post_value})
    else:
        if not post_key in l_posts[elements_current_index]:
            l_posts[elements_current_index][post_key] = post_value
        else:
            l_posts.append({post_key: post_value})
    return l_posts


def parse_list_raw_urns(l_raw_urns):
    """Iterates a list containing posts URNS and retrieves list of URNs

    :param l_raw_urns: List containing posts URNs
    :type l_raw_posts: list

    :return: List of URNs
    :rtype: list
    """
    l_urns = []
    for i in l_raw_urns:
        l_urns.append(get_urn_from_raw_update(i))
    return l_urns


def parse_list_raw_posts(l_raw_posts, linkedin_base_url):
    """Iterates a unsorted list containing post fields and assemble a
    list of dicts, each one of them contains a post

    :param l_raw_posts: Unsorted list containing posts information
    :type l_raw_posts: list
    :param linkedin_base_url: Linkedin URL
    :type linkedin_base_url: str

    :return: List of dicts, each one of them is a post
    :rtype: list
    """
    l_posts = []
    for i in l_raw_posts:
        author_name = get_update_author_name(i)
        if author_name:
            l_posts = append_update_post_field_to_posts_list(
                i, l_posts, "author_name", author_name
            )

        author_profile = get_update_author_profile(i, linkedin_base_url)
        if author_profile:
            l_posts = append_update_post_field_to_posts_list(
                i, l_posts, "author_profile", author_profile
            )

        old = get_update_old(i)
        if old:
            l_posts = append_update_post_field_to_posts_list(i, l_posts, "old", old)

        content = get_update_content(i, linkedin_base_url)
        if content:
            l_posts = append_update_post_field_to_posts_list(
                i, l_posts, "content", content
            )

        url = get_update_url(i, linkedin_base_url)
        if url:
            l_posts = append_update_post_field_to_posts_list(i, l_posts, "url", url)

    return l_posts


def get_list_posts_sorted_without_promoted(l_urns, l_posts):
    """Iterates l_urns and looks for corresponding dicts in l_posts matching 'url' key.
    If found, removes this dict from l_posts and appends it to the returned list of posts

    :param l_urns: List of posts URNs
    :type l_urns: list
    :param l_posts: List of dicts, which each of them is a post
    :type l_posts: list

    :return: List of dicts, each one of them is a post
    :rtype: list
    """
    l_posts_sorted_without_promoted = []
    l_posts[:] = [d for d in l_posts if "Promoted" not in d.get("old")]
    for urn in l_urns:
        for post in l_posts:
            if urn in post["url"]:
                l_posts_sorted_without_promoted.append(post)
                l_posts[:] = [d for d in l_posts if urn not in d.get("url")]
                break
    return l_posts_sorted_without_promoted


def generate_trackingId_as_charString():
    """Generates and returns a random trackingId

    :return: Random trackingId string
    :rtype: str
    """
    random_int_array = [random.randrange(256) for _ in range(16)]
    rand_byte_array = bytearray(random_int_array)
    return "".join([chr(i) for i in rand_byte_array])


def generate_trackingId():
    """Generates and returns a random trackingId

    :return: Random trackingId string
    :rtype: str
    """
    random_int_array = [random.randrange(256) for _ in range(16)]
    rand_byte_array = bytearray(random_int_array)
    return str(base64.b64encode(rand_byte_array))[2:-1]


def build_variable_for_search_query(keywords, offset_placeholder="{offset}", **kwargs):
    filters = []
    for key, value in kwargs.items():
        if value is not None and value != "" and value != []:
            if isinstance(value, list):
                value_list = ','.join(map(str, value))
                filters.append(f"(key:{key},value:List({value_list}))")
            else:
                filters.append(f"(key:{key},value:List({value}))")
    if filters:
        variables = f"variables=(start:{offset_placeholder},origin:FACETED_SEARCH,query:(keywords:{','.join(keywords)},flagshipSearchIntent:SEARCH_SRP,queryParameters:List({','.join(filters)}),includeFiltersInResponse:false))&&queryId=voyagerSearchDashClusters.b0928897b71bd00a5a7291755dcd64f0"
        return variables
    else:
        return ""
    
def get_entity_attribute(entity, keys):
        if isinstance(keys, str):
            keys = [keys]

        current_entity = entity
        for key in keys:
            current_entity = current_entity.get(key)
            if not current_entity:
                return ""

        return current_entity

def fetch_necessary_results_from_search_data(employees_data):
    results = []

    for cluster in employees_data.get("elements", []):
        if cluster.get("_type") != "com.linkedin.voyager.dash.search.SearchClusterViewModel":
            continue

        for item in cluster.get("items", []):
            if item.get("_type") != "com.linkedin.voyager.dash.search.SearchItem":
                continue

            entity_result = item.get("item", {}).get("entityResult")
            if not entity_result or entity_result.get("_type") != "com.linkedin.voyager.dash.search.EntityResultViewModel":
                continue
            try:
                try:
                    member_distance = get_entity_attribute(entity_result, ["entityCustomTrackingInfo", "memberDistance"])
                    distance = int(''.join(filter(str.isdigit, member_distance)))
                except ValueError:
                    distance = 0

                employee =  {
                    "urn_id": get_entity_attribute(entity_result, "entityUrn").split(":fsd_profile:")[1].split(",")[0],
                    "distance": distance,
                    "jobtitle": get_entity_attribute(entity_result, ["primarySubtitle", "text"]),
                    "location": get_entity_attribute(entity_result, ["secondarySubtitle", "text"]),
                    "name": get_entity_attribute(entity_result, ["title", "text"]),
                }
                print(employee["name"])
                results.append(employee)
            except Exception as e:
                print(f"Exception {e} occurred while processing search data")
                exit(1)
     
        return results