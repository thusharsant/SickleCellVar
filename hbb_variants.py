import requests
import pandas as pd
from typing import List, Dict, Any
import time

def get_hbb_variants() -> pd.DataFrame:
    """
    Fetches all known variants for the HBB gene from Ensembl REST API.
    
    Returns:
        pd.DataFrame: DataFrame containing variant information with columns:
            - rsID: Reference SNP ID
            - variant_type: Type of variant
            - start: Start position
            - end: End position
            - consequence: Variant consequence
    """
    # HBB gene coordinates on chromosome 11
    chrom = "11"
    start = 5227002
    end = 5229002
    
    # Ensembl REST API endpoint
    url = f"https://rest.ensembl.org/overlap/region/human/{chrom}:{start}-{end}?feature=variation"
    
    # Set headers for JSON response
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        # Make the API request
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise exception for bad status codes
        
        # Parse the JSON response
        variants = response.json()
        
        # Process the variants into a DataFrame
        variant_data = []
        for variant in variants:
            variant_data.append({
                'rsID': variant.get('id', ''),
                'variant_type': variant.get('var_class', ''),
                'start': variant.get('start', ''),
                'end': variant.get('end', ''),
                'consequence': variant.get('consequence_type', '')
            })
        
        # Create and return DataFrame
        return pd.DataFrame(variant_data)
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching variants: {e}")
        return pd.DataFrame()

def get_variant_annotations(rsids: List[str]) -> pd.DataFrame:
    """
    Queries the Ensembl VEP API to retrieve annotations for a list of rsIDs.
    
    Args:
        rsids (List[str]): List of rsIDs to query (e.g. ['rs334', 'rs33930165'])
    
    Returns:
        pd.DataFrame: DataFrame containing variant annotations with columns:
            - rsID: Reference SNP ID
            - clinical_significance: Clinical significance of the variant
            - most_severe_consequence: Most severe consequence
            - gene_symbol: Affected gene symbol
            - allele_frequencies: Dictionary of population allele frequencies
    """
    variant_data = []
    
    for rsid in rsids:
        # Ensembl VEP API endpoint for single variant
        url = f"https://rest.ensembl.org/vep/human/id/{rsid}?"
        
        # Set headers for JSON response
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        try:
            # Make the API request
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            # Parse the JSON response
            data = response.json()
            
            if not data:
                print(f"No data found for {rsid}")
                continue
                
            # Process the first (and usually only) result
            variant = data[0]
            
            # Extract clinical significance
            clinical_significance = []
            if 'colocated_variants' in variant:
                for colocated in variant['colocated_variants']:
                    if 'clin_sig' in colocated:
                        if isinstance(colocated['clin_sig'], list):
                            clinical_significance.extend(colocated['clin_sig'])
                        else:
                            clinical_significance.append(colocated['clin_sig'])
            
            # Extract most severe consequence
            most_severe_consequence = variant.get('most_severe_consequence', '')
            
            # Extract gene symbol
            gene_symbol = ''
            if 'transcript_consequences' in variant:
                for transcript in variant['transcript_consequences']:
                    if transcript.get('canonical', 0) == 1:
                        gene_symbol = transcript.get('gene_symbol', '')
                        break
            
            # Extract population frequencies
            allele_frequencies = {}
            if 'colocated_variants' in variant:
                for colocated in variant['colocated_variants']:
                    if 'frequencies' in colocated:
                        for pop, freq in colocated['frequencies'].items():
                            if pop in ['sas', 'afr', 'eur']:  # Note: API returns lowercase population codes
                                allele_frequencies[pop.upper()] = freq
            
            variant_data.append({
                'rsID': rsid,
                'clinical_significance': ','.join(clinical_significance) if clinical_significance else '',
                'most_severe_consequence': most_severe_consequence,
                'gene_symbol': gene_symbol,
                'SAS_freq': allele_frequencies.get('SAS', ''),
                'AFR_freq': allele_frequencies.get('AFR', ''),
                'EUR_freq': allele_frequencies.get('EUR', '')
            })
            
            # Add a small delay to avoid hitting rate limits
            time.sleep(0.1)
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {rsid}: {e}")
            continue
    
    # Create and return DataFrame
    return pd.DataFrame(variant_data)

if __name__ == "__main__":
    # Example usage for both functions
    print("HBB Variants:")
    variants_df = get_hbb_variants()
    print(variants_df.head())
    
    print("\nVariant Annotations:")
    test_rsids = ['rs334', 'rs33930165']
    annotations_df = get_variant_annotations(test_rsids)
    pd.set_option('display.max_columns', None)  # Show all columns
    print(annotations_df) 