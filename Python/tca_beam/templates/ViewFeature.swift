// MARK: - Reducer

public struct {{ featureName }}: ReducerProtocol {
    public struct State: Equatable {
        // Beam-TODO: add your states here for this reducer
{% if subReducerFeatures|length > 0 %}
        // sub-reducer states
{%- for subFeatureKey, subFeatureValue in subReducerFeatures.items() %}
        var {{ subFeatureValue.varName }}: {{ subFeatureValue.featureName }}.State
{%- endfor -%}
{% endif %}
    }

    public enum Action: BindableAction, Equatable {
        case binding(BindingAction<State>)

        // Beam-TODO: add your actions here for this reducer
{% if subReducerFeatures|length > 0 %}
        // sub-reducer actions
{%- for subFeatureKey, subFeatureValue in subReducerFeatures.items() %}
        case {{ subFeatureValue.varName }}({{ subFeatureValue.featureName }}.Action)
{%- endfor -%}
{% endif %}
    }

    public var body: some ReducerProtocol<State, Action> {
        BindingReducer()
{%- if subReducerFeatures|length > 0 %}
        // scope in the reducers for sub-reducers
{%- for subFeatureKey, subFeatureValue in subReducerFeatures.items() %}
        Scope(state: \.{{ subFeatureValue.varName }}, action: /Action.{{ subFeatureValue.varName }}) {
            {{ subFeatureValue.featureName }}()
        }
{%- endfor %}
{%- endif %}
        // reducer for this feature
        Reduce<State, Action> { state, action in
            switch action {

            default:
                return .none
            }
        }
{%- if subReducerFeatures|length > 0 %}
        // reducer for sub-feature actions
        Reduce<State, Action> { state, action in
            switch action {

            // Beam-TODO: deal with these actions from sub-reducers
{%- for subFeatureKey, subFeatureValue in subReducerFeatures.items() %}

            case let .{{ subFeatureValue.varName }}({{ subFeatureValue.varName }}Action):
                return .none
{%- endfor %}

            default:
                return .none
            }
        }
{% endif %}
    }
}
